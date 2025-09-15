from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/servicio/ejemplo')
def servicioEjemplo():
    data = { "status" : "OK", "msg" : "Microservicio de ejemplo..."} 
    return jsonify(data)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=81, debug=True)
