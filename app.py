from flask import Flask
import os
import database as db
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'login-registro')

app = Flask(__name__,template_folder = 'login-registro')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('login.html')   

@app.route('/inicio')
def inicio():
    return render_template('inicioA.html') 

@app.route('/citas')
def citas():
    return render_template('citas.html') 

 




# ACCESO---LOGIN
@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
       
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol']=account['id_rol']
            
            if session['id_rol']==1:
                return render_template("inicioA.html")
            if session ['id_rol']==2:
                return render_template("index.html")
            
        else:
            return render_template('login.html',mensaje="Usuario O Contraseña Incorrectas")

#registro---
@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/crear-registro', methods= ["GET", "POST"])
def crear_registro(): 
    
    correo=request.form['txtCorreo']
    password=request.form['txtPassword']
    
    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, '2')",(correo,password))
    mysql.connection.commit()
    return render_template("login.html",mensaje2="Usuario Registrado Exitosamente")


@app.route('/crud')
def crud():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('crud.html', data=insertObject)

#Ruta para guardar usuarios en la bdd
@app.route("/user", methods=["POST"])
def addUser():
    Salon = request.form['salon']
    Servicios = request.form['servicios']
    

    if Salon and Servicios:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (salon, servicios) VALUES (%s, %s)"
        data = (Salon, Servicios)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('crud'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('crud'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    Salon = request.form['salon']
    Servicios = request.form['servicios']
    

    if Salon and  Servicios:
        cursor = db.database.cursor()
        sql = "UPDATE users SET salon = %s, servicios = %s WHERE id = %s"
        data = (Salon, Servicios, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('crud'))

    
    
    











if __name__ == '__main__':
    app.secret_key="paty9721"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    