#!flask/bin/python
from flask import Flask, jsonify, abort, request, url_for
import random, time

app = Flask(__name__)

medidor = [{
        'id': 0,
}]

def make_public_medida(medida):
    new_medida = {}
    #for field in medida:
        #if field == 'id':
        #    new_medida['uri'] = url_for('get_medida', medida_id=medida['id'], _external=True)
        #else:
         #   new_medida[field] = medida[field]
    #return new_medida
    return medida

@app.route('/', methods=['GET'])
def get_medidor():
    return jsonify({'medidor': medidor})

    
@app.route('/', methods = ['POST'])
def create_medida():
    if not request.json or not 'valor' in request.json:
        abort(400)
    medida = {
        'id': medidor[-1]['id'] + 1,
        'idMedidor': request.json['idMedidor'],
        'valor': request.json['valor'],
        'timestamp': request.json.get('timestamp', ""),
        'timestampServer': time.time()
        #'total': False
    }
    medidor.append(medida)
    return jsonify( { 'medida': make_public_medida(medida) } ), 201


@app.route('/<int:medida_id>', methods=['GET'])
def get_medida(medida_id):
    medida = [medida for medida in medidor if medida['id'] == medida_id]
    if len(medida) == 0:
        abort(404)
    return jsonify({'medida': medida[0]})
    
@app.route('/medidor/<string:medidor_id>', methods=['GET'])
def get_medidas(medidor_id):
    medida = [medida for medida in medidor if medida['idMedidor'] == medidor_id]
    if len(medida) == 0:
        abort(404)
    return jsonify({'medida': medida[0]})

if __name__ == '__main__':
    app.run(debug=True)
