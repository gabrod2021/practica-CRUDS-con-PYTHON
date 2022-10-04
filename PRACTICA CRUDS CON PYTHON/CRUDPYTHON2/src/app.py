from flask import Flask ,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:TitoPitbull@localhost/flaskmysql'
#                                          usuario:clave@localhost/nombreBaseDeDAtos
#                                          usuario:clave@localhost/nombreBaseDeDAtos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)
ma=Marshmallow(app)
class Producto(db.Model):  # defino la tabla
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    def __init__(self,nombre,precio,stock):
        self.nombre=nombre
        self.precio=precio
        self.stock=stock
db.create_all()  # crea las tablas 
class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock')
 
producto_schema=ProductoSchema()            # para crear un producto
productos_schema=ProductoSchema(many=True)  # multiples registros-Creo las rutas o endpoints
 
@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()
    result=productos_schema.dump(all_productos)
    return jsonify(result)
 # producto en singular, cuando la consulta es por ID
@app.route('/producto/<id>', methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)

@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    new_producto=Producto(nombre,precio,stock)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)

# producto en singular, cuando la consulta es por ID
@app.route('/producto/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=Producto.query.get(id)#<---ID ESTABA COMO STRING ENTRE COMILLAS
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    producto.nombre=nombre
    producto.precio=precio
    producto.stock=stock
    db.session.commit()#<---FALTABAN LOS PARENTESIS EN EL COMIT
    return producto_schema.jsonify(producto)

# producto en singular, cuando la consulta es por ID
@app.route('/producto/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)

 
# programa principal
if __name__=='__main__':  
    app.run(debug=True, port=5000)   
