import mysql.connector

# Conexión a la BD
try:
    conexion = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = ''
    )
    print("Conectado a la base de datos")
except Exception as e:
    print(f"Error en la conexion de la BD: {e}" )

# Cursor que permite la ejecución de instrucciones sql
cursor = conexion.cursor()