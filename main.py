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

# Creación de la base de datos
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS CompanyData")
    print("Base de datos creada")
except Exception as e:
    print(f"Error al crear la base de datos: {e}")

# Usar la base de datos
cursor.execute("USE CompanyData")

# Creación de la tabla
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EmployeePerformance (
            id INT PRIMARY KEY AUTO_INCREMENT,
            employee_id INT,
            department VARCHAR(40),
            performance_score FLOAT,
            years_with_company INT,
            salary FLOAT
        )
    """)
except Exception as e:
    print(f"Error al crear la tabla: {e}")    