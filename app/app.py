from flask import Flask,render_template, redirect, request, url_for
import mysql.connector
#crear instancia

app = Flask (__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda2025"
)
cursor = db.cursor()
db.commit()

    
@app.route('/')
def Lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas')
    usuario = cursor.fetchall()

    return render_template('index.html', personas=usuario)
    
@app.route('/Registrar', methods=['GET','POST'])
def registrar_usuario():
    if request.method == 'POST':
       NOMBRE = request.form.get('NOMBRE')
       APELLIDOS = request.form.get('APELLIDOS')
       CORREO_ELECTRONICO = request.form.get('EMAIL')
       DIRECCION = request.form.get('DIRECCION')
       TELEFONO = request.form.get('TELEFONO')
       USUARIO = request.form.get('USUARIO')
       CONTRASENA = request.form.get('CONTRASENA')

        #insertar datos

       cursor.execute("INSERT INTO personas(nombre,apellido,email_persona,direccion,telefono,usuario,contrasena)values(%s,%s,%s,%s,%s,%s,%s)",(NOMBRE,APELLIDOS,CORREO_ELECTRONICO,DIRECCION,TELEFONO,USUARIO,CONTRASENA))
       db.commit()
       

       #redirigir a la misma  pagina cuando el metodo es POST 
       return redirect(url_for('registrar_usuario'))

    #Si es un metodo GET me renderiza al formulario
    return render_template('Registrar.html')

@app.route('/editar/<int:codigo>',methods=['POST','GET'])
def editar_usuario(codigo):
    cursor = db.cursor()
    if request.method == 'POST':
        nombreperso = request.form.get('nombreperso')
        apellidoperso = request.form.get('apellidoperso')
        correoperso =  request.form.get('correoperso')
        direccionperso = request.form.get('direccionperso')
        telefonoperso = request.form.get('telefonoperso')
        usuarioperso = request.form.get('usuarioperso')
        passwordperso = request.form.get('passwordperso')


        sql = "UPDATE personas set nombre_persona=%s,apellido_persona=%s,direccion=%s,email_persona=%s,telefono=%s,usuario=%s,contrasena=%s where codigoperso=%s"
        nombreperso = request.form.get['nombreperso']
        cursor.execute(sql,(nombreperso,apellidoperso,direccionperso,correoperso,telefonoperso,usuarioperso,passwordperso,codigo))
        db.commit()

        return redirect(url_for('Lista'))
    else:
        #obtener datos de la persona 
        cursor = db.cursor()
        cursor.execute('SELECT * FROM personas WHERE id_perso = %s',(codigo,))
        data = cursor.fetchall()

        return render_template('editar.html', personas=data[0])
    
@app.route('/eliminar/<int:codigo>', methods=['GET'])
def eliminar_usuario(codigo):

    return redirect(url_for('Lista'))

if __name__=='__main__':
    app.add_url_rule('/',view_func=Lista)
    app.run(debug=True,port=5005)

    #definir rutas