from flask import Flask, request, url_for, session, json, jsonify, redirect
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
from datetime import datetime
from flask_mail import Mail, Message
import MySQLdb.cursors
import secrets
import base64
import hashlib
from flask import Flask
import pymysql

application = app = Flask(__name__)
CORS(app, support_credentials=True)

# SECRET KEY
app.secret_key = secrets.token_hex(16)

# DATABASE CONFIG
app.config['MYSQL_HOST'] = 'delfostalent-instance-1.cmw5apadqru8.us-west-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'cmolina'
app.config['MYSQL_PASSWORD'] = 'KC1zMMF%0^Xl'
app.config['MYSQL_DB'] = 'app_cmp_mirror'

# INICIALIZA MYSQL
mysql = MySQL(app)

secret_key = "testing"

#OBTENEMOS BANDEJA     /bandeja/u=cmp2020 
@app.route('/bandeja/', methods=['GET'])
def bandeja():

    if request.method == 'GET':
        
        token1 = request.values.get('tk')
        usuario = request.values.get('u')

        ##SIN TOKEN POR AHORA
        # if token1 is None:
        #  token1 = 'none'
        # secret = usuario+secret_key
        # token2 = hashlib.md5(secret.encode())
        # token2 = token2.hexdigest()
        
        # VALIDA API TOKEN
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #conexion con mysql
        #cursor.execute('SELECT id FROM app_accesos WHERE id_usuario = "'+usuario+'" ')
        cursor.execute('SELECT id FROM app_accesos WHERE id_usuario = "'+usuario+'" ')
   
        mysql.connection.commit() #ejecutamos consulta
        result = cursor.fetchone()
       
        now = datetime.now()
        fecha_hoy = now.strftime("%d-%m-%Y %H:%M:%S")

        if result is not None:
         id_usuario = result['id']
        else:
         id_usuario = 0
        print(id_usuario)
        if id_usuario > 0:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT ab.id_solicitud,ab.id, CASE WHEN ab.id_solicitud = 1 THEN 'Transporte' WHEN ab.id_solicitud = 2 THEN 'Prestamo Sueldo Base' WHEN ab.id_solicitud = 3 THEN 'Anticipo' WHEN ab.id_solicitud = 4 THEN 'Asignación'  WHEN ab.id_solicitud = 5 THEN 'Beca Jaime Arbildúa'  WHEN ab.id_solicitud = 51 THEN 'Beca Enseñanza Media'  WHEN ab.id_solicitud = 52 THEN 'Beca Enseñanza Superior' WHEN ab.id_solicitud = 53 THEN 'Beca Enseñanza Pre Básica' WHEN ab.id_solicitud = 54 THEN 'Beca Enseñanza Básica'  WHEN ab.id_solicitud = 55 THEN 'Beca E. Media Excelencia A.' WHEN ab.id_solicitud = 56 THEN 'Beca Continuidad de Estudios' WHEN ab.id_solicitud = 57 THEN 'Beca E.Académica Rol PDP' WHEN ab.id_solicitud = 58 THEN 'Beca Postgraod 2021'  WHEN ab.id_solicitud = 7 THEN 'Venta de Vacaciones' WHEN ab.id_solicitud = 41 THEN 'Asignación Matricula'     ELSE 'Otro' END AS 'Solicitud', ab.fecha_creacion, ab.estado AS estado_bandeja FROM app_bandeja ab  LEFT JOIN app_transporte_solicitud ts ON ts.id_bandeja = ab.id  LEFT JOIN app_beneficio_solicitud b ON b.id_bandeja = ts.id WHERE  ab.estado != 9 AND ab.id_usuario = "+str(id_usuario)+" ")
            #cursor.execute("SELECT  * FROM app_accesos ")

            mysql.connection.commit()
            data = cursor.fetchall()
            cursor.close()
            return jsonify(data)
        else:
            return '0'  
             
    else:
        return '0'


@app.route('/')
def Index():
    return 'Extensión /query1, /query2... /query6. Además se encuentra "/bandeja/u=cmp2020" siendo cmp2020 el usuario en este ejemplo. También se encuentra "/users/activos?user=eduardo" que son los usuarios activos en el sistema con primero nombre eduardo'


#Query movidicar relacionada con modificar estado de 
@app.route('/info')
def inf():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT b.id, b.id_solicitud, b.estado  FROM app_cmp_mirror.app_bandeja b')
    data = cursor.fetchall()
    #print(data)
    return jsonify(data)   


@app.route('/info/update/<id>', methods=['PUT'])
def mod(id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE app_bandeja SET estado = "9" WHERE Id = %s', (id,))
        data = cursor.fetchone()
        mysql.connection.commit()
        resp = jsonify(data)
        #resp.status_code = 200
        return resp
    
# Query1: Trae todo de app_accesos
@app.route('/query1')
def Query1():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('Select * FROM app_accesos ')
    data = cursor.fetchall()
    #print(data)
    return jsonify(data)   


@app.route('/users/activos')
def activos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user = request.values.get('user')
    cursor.execute('SELECT c.Id, c.FichaSap, c.Nombre, c.Email, c.telefono, c.direccion FROM app_personal_maestro pm LEFT JOIN app_celulas c ON c.FichaSAP = pm.nro WHERE pm.nombre_search like "'+user+'%" group by c.FichaSAP')
    
    data = cursor.fetchall()
    #print(data)
    return jsonify(data) 

    
##FUNCIONA INSERT
@app.route('/users/insert', methods=['GET','POST'])
def insertar():
#    try:
    if request.method == 'POST':
        
        codigo = request.form.get('codigo')
        nombre = request.form.get('nombre')
        creditos = request.form.get('creditos')
        print (creditos)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO testing (codigo, nombre, creditos) VALUES (%s, %s, %s)', (codigo, nombre, creditos))
        #cursor.execute('INSERT INTO testing VALUES (codigo="'+codigo+'", nombre="'+nombre+'", creditos="'+creditos+'") ')
        data = cursor.fetchone()
        
        #data = cursor.fetchall()
        mysql.connection.commit()
        print(request.json)
        return jsonify({'mensaje': "Curso registrado"})
 #   except Exception as ex:
        #return jsonify({'mensaje': "error"})
    else:
         return '0'

# para actualizar el estado al hacer click y dejarlo en 9 o desactivado
@app.route('/users/deactivate/<id>', methods=['PUT'])
def deact_user(id):
        #id=id
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #id = request.args.get('id')
        #print(id)
        cursor.execute('UPDATE app_accesos SET estado = "9" WHERE Id = %s', (id,))
        #cursor.execute('UPDATE testing SET estado = "9" WHERE Id = 3')
        data = cursor.fetchone()
        mysql.connection.commit()
        resp = jsonify(data)
        #resp.status_code = 200
        return resp

# para actualizar el estado al hacer click y dejarlo en 0 o Activado
@app.route('/users/activate/<id>', methods=['PUT'])
def act_user(id):
        #id=id
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #id = request.args.get('id')
        #print(id)
        cursor.execute('UPDATE app_accesos SET estado = "0" WHERE Id = %s', (id,))
        #cursor.execute('UPDATE testing SET estado = "9" WHERE Id = 3')
        data = cursor.fetchone()
        mysql.connection.commit()
        resp = jsonify(data)
        #resp.status_code = 200
        return resp        

@app.route('/users/update/name', methods=['POST'])
def edit_name():
    id = request.form.get('pk')
    name = request.form.get('value')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #cursor.execute('UPDATE app_accesos SET nombre ="%s" WHERE id= %s', (nombre, id))
    cursor.execute('UPDATE app_accesos SET nombre =%s WHERE id=%s ', (name,id)) #funcionando bien, poniendo el nombre/id
    
    #cursor.execute('UPDATE app_accesos SET nombre =%s WHERE id="1" ', (nombre,)) funciona
    #cursor.execute('UPDATE app_accesos SET nombre = "nombre" WHERE id="1"') #Funciona cuando el valor que s ele pasa en la direccion es igual a la que se pasa al nombre
    data = cursor.fetchone()
    mysql.connection.commit()
    resp = jsonify(data)
    #resp.status_code = 200
    return resp  


@app.route('/users/update/email', methods=['POST'])
def edit_email():
    id = request.form.get('pk')
    email = request.form.get('value')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE app_accesos SET email = %s WHERE id= %s', (email,id)) #funcionando bien
    #cursor.execute('UPDATE app_accesos SET email ="nuevojuanpablo.saez@grupoavanza.com" WHERE id= %s', (id,))
    #UPDATE app_accesos SET email ='nuevojuanpablo.saez@grupoavanza.com' WHERE id='1'
    data = cursor.fetchone()
    mysql.connection.commit()
    resp = jsonify(data)
    #resp.status_code = 200
    return resp  

    return '0'



@app.route('/usuarios/registro', methods=['POST'])
def registrar():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    datos = request.form.get("detalle")
    cursor.execute('INSERT INTO app_registro_usuario (datos) VALUES (%s)', (datos) )
    #cursor.execute('INSERT INTO app_registro_usuario (datos) VALUES ("felipe molina, grupo avanza")')
    #INSERT INTO testing (codigo, nombre, creditos) VALUES (%s, %s, %s)', (codigo, nombre, creditos)
    data = cursor.fetchone()
    mysql.connection.commit()
    resp = jsonify(data)
    return resp 



#Query2: Ordenada por tipo solicitud ( Beneficios y transporte); se muestra la cantidad de solicitudes y el tipo de solicitud.
@app.route('/query2')
def Query2():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT count(s.tipo) AS Cantidad_solicitudes, s.tipo AS TIPO_SOLICITUD FROM app_bandeja b INNER JOIN app_solicitud s ON s.id = b.id_solicitud WHERE s.id = b.id_solicitud group by s.tipo')
    data = cursor.fetchall()
    #print(data)
    return jsonify(data)   

#Query3: Cantidad de solicitudes de tipo "Beca" por división; se  muestra la cantidad y el nombre de la división.
@app.route('/query3')
def Query3():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT count(*) AS Cantidad_Solicitudes, pm.division, s.solicitud FROM app_bandeja b INNER JOIN app_solicitud s ON s.id = b.id_solicitud LEFT JOIN app_personal_maestro pm ON pm.id = b.id_usuario WHERE b.id_solicitud = 5 group by pm.division')
    data = cursor.fetchall()
    #print(data)
    return jsonify(data)   

#Query4: Cantidad de licencias ordenadas según el tipo que sean; se muestra la cantidad y el tipo.
@app.route('/query4')
def Query4():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT count(*) AS Cantidad_Solicitudes, li.tipo_licencia FROM app_licencias li, app_personal_maestro pm WHERE pm.nro = li.nro_ficha group by li.tipo_licencia')
    data = cursor.fetchall()
    #print(data)
    return jsonify(data)   

#Query5: Cantidad de licencias ordenadas según la división; se muestra la cantidad de licencias y la división.
@app.route('/query5')
def Query5():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT count(*) AS Cantidad_Licencias, pm.division FROM app_licencias li, app_personal_maestro pm WHERE pm.nro = li.nro_ficha group by pm.division')
    data = cursor.fetchall()
    #print(data)
    return jsonify(data)   

#Query6: Cantidad de licencias por subdivisión; se muestra la cantidad de licencias y subdivisión.
@app.route('/query6')
def Query6():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT count(*) AS Cantidad_Licencias, pm.subdivision FROM app_licencias li, app_personal_maestro pm WHERE pm.nro = li.nro_ficha group by pm.subdivision')
    data = cursor.fetchall()
    #print(data)
    return jsonify(data)   

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)