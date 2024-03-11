from flask import Flask,render_template, redirect, request,url_for,flash,bcrypt
import mysql.connector
import bcrypt
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

def encriptarcontra(contraencrip):
    #generar un hash de la contraseña mejor dicho un encriptado
    encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'),bcrypt.gensalt())
    
    return encriptar
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
       
       contrasenaencriptada = encriptarcontra(CONTRASENA)

        #insertar datos

       cursor.execute("INSERT INTO personas(nombre,apellido,email_persona,direccion,telefono,usuario,contrasena)values(%s,%s,%s,%s,%s,%s,%s)",
                      (NOMBRE,APELLIDOS,CORREO_ELECTRONICO,DIRECCION,TELEFONO,USUARIO,contrasenaencriptada))
       db.commit()
       

       #redirigir a la misma  pagina cuando el metodo es POST 
       return redirect(url_for('registrar_usuario'))

    #Si es un metodo GET me renderiza al formulario
    return render_template('Registrar.html')

@app.route('/editar/<int:codigo>',methods=['POST','GET'])
def editar_usuario(codigo):
    cursor = db.cursor()
    if request.method == 'POST':
        nombrep = request.form.get('nombre')
        apellidop = request.form.get('apellido')
        correop =  request.form.get('email_persona')
        telefonop = request.form.get('telefono')
        usuariop = request.form.get('usuario')
        passwordp = request.form.get('contrasena')
        direccionp = request.form.get('direccion')


        sql = "UPDATE personas set nombre=%s,apellido=%s,direccion=%s,email_persona=%s,telefono=%s,usuario=%s,contrasena=%s where id_perso=%s"
        cursor.execute(sql, (nombrep,apellidop,direccionp,correop,telefonop,usuariop,passwordp,codigo))
        db.commit()

        return redirect(url_for('Lista'))
    else:
        #obtener datos de la persona 
        cursor = db.cursor()
        cursor.execute('SELECT * FROM personas WHERE id_perso = %s',(codigo,))
        data = cursor.fetchall()
    if data:    

        return render_template('editar.html', personas=data[0])
    else:
        flash('usuario no encontrado','error')
        return redirect(url_for('lista'))
    
@app.route('/eliminar/<int:codigo>', methods=['GET'])
def eliminar_usuario(codigo):
    cursor = db.cursor()

    if request.method == 'POST':
        cursor.execute('DELETE FROM personas WHERE Idpersona = %s' (codigo))
        db.commit()
        flash('Este usuario se elimino correctamente', 'success')
        return redirect(url_for('Lista'))
    
    else:
        cursor.execute('SELECT * FROM personas WHERE Idpersona = %s', (codigo))
        data = cursor.fetchone()

        if data:
            return render_template('eliminar.html', personas=data)
        
if __name__=='__main__':
    app.add_url_rule('/',view_func=Lista)
    app.run(debug=True,port=5005)

    #definir rutas