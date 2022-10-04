from flask import Flask,jsonify,request
from productos import productos
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/productos')
def getproductos():
    return jsonify(productos)

@app.route('/productos/<string:product_name>')
def getproducto( product_name):
    productoEncontrado=[ producto for producto in productos if producto["nombre"]==product_name]
    if len(productoEncontrado)>0:
        return jsonify(productoEncontrado[0])
    else:
        return "no encontrado"

@app.route('/productos', methods=["POST"])
def agregarProducto():
    new_producto={
        "nombre":request.json['nombre'],
        "precio":request.json['precio'],
        "stock":request.json['stock'],
    }
    productos.append(new_producto)
    return jsonify({"productos": productos })

#PROGRAMA PRINCIPAL
if __name__=='__main__':         
    app.run(debug=True, port=5000)  
    