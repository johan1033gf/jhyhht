from flask import Flask, render_template, redirect, request, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Crear instancia
app = Flask(__name__)
app.secret_key = '405025'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda2025"
)
cursor = db.cursor()
db.commit()

@app.route('/password/<contraencrip>')
def encriptarcontra(contraencrip):
    # Generar un hash de la contraseña, mejor dicho un encriptado
    encriptar = generate_password_hash(contraencrip)
    valor = check_password_hash(encriptar, contraencrip)

    return "Encriptado:{0} | coincide:{1}".format(encriptar, valor)

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        # Verificar las credenciales del usuario
        username = request.form.get('txtusuario')
        password = request.form.get('txtcontrasena')

        cursor = db.cursor()
        cursor.execute("SELECT usuario, contrasena FROM personas WHERE usuario = %s", (username,))
        resultado = cursor.fetchone()

        if resultado and check_password_hash(resultado[1], password):
            session['usuarios'] = username
            return redirect(url_for('lista'))
        else:
            error = 'Credenciales invalidas. por favor intentarlo de nuevo'
            return render_template('Login.html', error=error)
       
    return render_template('Login.html')

@app.route('/')
def lista():
    if 'usuarios' in session:
        cursor.execute('SELECT * FROM personas')
        usuario = cursor.fetchall()
        return render_template('index.html', personas=usuario)
    else:
        return redirect(url_for('Login'))

@app.route('/Registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        NOMBRE = request.form.get('NOMBRE')
        APELLIDOS = request.form.get('APELLIDOS')
        CORREO_ELECTRONICO = request.form.get('EMAIL')
        DIRECCION = request.form.get('DIRECCION')
        TELEFONO = request.form.get('TELEFONO')
        USUARIO = request.form.get('USUARIO')
        CONTRASENA = request.form.get('CONTRASENA')
        
        contrasenaencriptada = generate_password_hash(CONTRASENA)

        # Insertar datos
        cursor.execute("INSERT INTO personas(nombre, apellido, email_persona, direccion, telefono, usuario, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (NOMBRE, APELLIDOS, CORREO_ELECTRONICO, DIRECCION, TELEFONO, USUARIO, contrasenaencriptada))
        db.commit()
        
        # Redirigir a la misma página cuando el método es POST
        return redirect(url_for('registrar_usuario'))

    # Si es un método GET, renderiza el formulario
    return render_template('Registrar.html')

@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombrep = request.form.get('nombre')
        apellidop = request.form.get('apellido')
        correop = request.form.get('email_persona')
        telefonop = request.form.get('telefono')
        usuariop = request.form.get('usuario')
        passwordp = request.form.get('contrasena')
        direccionp = request.form.get('direccion')

        sql = "UPDATE personas SET nombre=%s, apellido=%s, direccion=%s, email_persona=%s, telefono=%s, usuario=%s, contrasena=%s WHERE id_perso=%s"
        cursor.execute(sql, (nombrep, apellidop, direccionp, correop, telefonop, usuariop, passwordp, id))
        db.commit()
        return redirect(url_for('lista'))
    else:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM personas WHERE id_perso = %s', (id,))
        data = cursor.fetchall()
        if data:
            return render_template('editar.html', personas=data[0])
        else:
            flash('usuario no encontrado', 'error')
            return redirect(url_for('lista'))

@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_usuario(id):
    if request.method == 'POST':
        cursor.execute('DELETE FROM Personas WHERE id_perso = %s', (id,))
        db.commit()
        return redirect(url_for('lista'))
    else:
        cursor.execute('SELECT * FROM personas WHERE id_perso = %s', (id,))
        data = cursor.fetchall()
        if data:
            return render_template('eliminar.html', Personas=data)

if __name__ == '__main__':
    app.add_url_rule('/', view_func=lista)
    app.run(debug=True, port=5005)