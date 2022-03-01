'''
Importaciones que se utilizan en el codigo
'''
from itertools import product
import json
import string
from flask import Flask, jsonify, request

app = Flask(__name__)

'''
Arreglo en el que se guardaran los productos, sera un arreglo de json
'''
products = []

'''
Metodo que se encarga de listar todos los productos devuelve un json
'''
@app.route('/products', methods=['GET'])
def getProducts():
 if request.method == 'GET':
    return jsonify(products)

'''
Metodo que se encarga de recorrer cada linea del archivo insertado y de guardar cada producto en el arreglo de productos
'''
@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
  archivo = request.files['archivo']
  for line in archivo:
      arreglo = str(line, encoding = "utf-8").split(',')
      nuevo_producto = {
        "id": int(arreglo[0]), 
        "serial": int(arreglo[1]), 
        "descripcion": arreglo[2], 
        "usuario": arreglo[3], 
        "cantidad": int(arreglo[4]), 
        "estado": arreglo[5]
      }
      products.append(nuevo_producto)

  return jsonify("Archivo subido exitosamente")

'''
Metodo que se encarga de eliminar un producto del arreglo
'''
@app.route("/delete/<int:id>", methods=['DELETE'])
def delete(id):
 if request.method == 'DELETE':
    for item in products:
      if ( item['id'] == id ):
          index = products.index(item)
          products.pop(index)

    return jsonify("Eliminado con exito")

'''
Metodo que se encarga de guardar un producto en el arreglo de productos
'''
@app.route("/crearProducto", methods=['POST'])
def crearProducto():
 if request.method == 'POST':
    data = json.loads(request.data)
    print('request', data['id'])
    id = len(products)+1

    nuevo_producto = {
        "id": id, 
        "serial": data['serial'], 
        "descripcion": data['descripcion'], 
        "usuario": data['usuario'], 
        "cantidad": data['cantidad'], 
        "estado": data['estado']
    }
    products.append(nuevo_producto)
    
 return jsonify("Producto creado exitosamente")

'''
Metodo que se encarga de editar un producto en el arreglo
'''
@app.route("/editarProducto", methods=['POST'])
def editarProducto():
 if request.method == 'POST':
    data = json.loads(request.data)
    
    for item in products:
      if ( item['id'] == data['id'] ):
          index = products.index(item)

    nuevo_producto = {
        "id": data['id'], 
        "serial": data['serial'], 
        "descripcion": data['descripcion'], 
        "usuario": data['usuario'], 
        "cantidad": data['cantidad'], 
        "estado": data['estado']
    }
    products[index]=nuevo_producto
    
 return jsonify("Producto editado exitosamente")

if __name__ == '__main__':
    app.run(debug=True, port=4000)