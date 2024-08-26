import mysql.connector
import csv

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


# Se insertan los datos desde el archivo csv
try:
    with open("EmployeePerformance.csv", mode="r") as data:
        info = csv.reader(data)
        # Para que salte la primer linea
        next(info)
        # Recorre por todos los elementos
        for row in info:
            cursor.execute(
                """
                INSERT INTO employeeperformance (employee_id, department, performance_score, years_with_company, salary)
                VALUES (%s, %s, %s, %s, %s)
                """, 
                (row[1], row[2], row[3], row[4], row[5]))
                
        # Luego se confirman los datos ingresados en la bd
        conexion.commit()
        print("Datos insertados correctamente")
except Exception as e:
    print(f"Error al insertar datos: {e}")