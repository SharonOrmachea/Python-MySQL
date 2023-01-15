from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@localhost:3306/python_project01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Creacion de tabla Categoria
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nombre = db.Column(db.String(100))
    cat_descripcion = db.Column(db.String(100))

    def __init__(self, cat_nombre, cat_descripcion):
        self.cat_nombre = cat_nombre
        self.cat_descripcion = cat_descripcion
        
db.create_all()

# Creacion de Esquema 
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nombre', 'cat_descripcion')

# una sola respuesta
categoria_schema = CategoriaSchema()

# Cuando sean muchas respuestas
categorias_schema = CategoriaSchema(many=True)


# Get all
@app.route('/categorias', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

# Get by id
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria_by_id(id):
    una_categoria = Categoria.query.get(id)
    result = categoria_schema.dump(una_categoria)
    return jsonify(result)

# Post
@app.route('/categoria', methods=['POST'])
def insert_categoria():
    cat_nombre = request.json['cat_nombre']
    cat_descripcion = request.json['cat_descripcion']

    nuevo_registro = Categoria(cat_nombre, cat_descripcion)

    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)

# PUT
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    upCat = Categoria.query.get(id)

    cat_nombre = request.json['cat_nombre']
    cat_descripcion = request.json['cat_descripcion']

    upCat.cat_nombre = cat_nombre
    upCat.cat_descripcion = cat_descripcion

    db.session.commit()

    return categoria_schema.jsonify(upCat)

# Delete
@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    delCat = Categoria.query.get(id)

    db.session.delete(delCat)
    db.session.commit()
    return categoria_schema.jsonify(delCat)

# Mensaje de Bienvenida
@app.route('/', methods=['GET'])

def index():
    return jsonify({'Mensaje': 'Bienvenido'})

if __name__=="__main__": 
    app.run(debug=True)