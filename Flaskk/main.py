from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'secret_key_provisional'

# URL de tu API de FastAPI
API_URL = "http://localhost:5000/v1/usuarios"

@app.route('/')
def index():
    # Consultar todos los usuarios (GET)
    response = requests.get(API_URL)
    data = response.json().get('data', [])
    return render_template('index.html', usuarios=data)

@app.route('/agregar', methods=['POST'])
def agregar():
    # Crear usuario (POST)
    nuevo_usuario = {
        "id": request.form['id'],
        "nombre": request.form['nombre'],
        "edad": request.form['edad']
    }
    response = requests.post(API_URL, json=nuevo_usuario)
    if response.status_code != 200:
        flash(f"Error: {response.json().get('detail')}")
    return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar(id):
    # Eliminar usuario (DELETE)
    requests.delete(f"{API_URL}/{id}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=8000, debug=True)