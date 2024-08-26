import mysql.connector
import csv
import pandas as pd
import matplotlib.pyplot as plt


class ConexionDB:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.conexion = None
        self.cursor = None


    def conectar(self):

        try:
            self.conexion = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password
            )
            self.cursor = self.conexion.cursor()
            print("Conectado a la base de datos")
        except Exception as e:
            print(f"Error en la conexion de la BD: {e}" )

    # Creación de la base de datos
    def crear_db(self, db_name):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print("Base de datos creada")
        except Exception as e:
            print(f"Error al crear la base de datos: {e}")

    # Para usar la base de datos
    def usar_db(self, db_name):
        self.cursor.execute(f"USE {db_name}")

    # Para la creacion de la tabla
    def crear_tabla(self, sql_tabla):
        try:
            self.cursor.execute(sql_tabla)
            print("Tabla creada")
        except Exception as e:
            print(f"Error al crear la tabla: {e}") 


    # Para insertar los datos
    def insertar_datos(self, nombre_tabla, datos_csv):
        try:
            with open(datos_csv, mode="r") as data:
                info = csv.reader(data)
                # Para que salte la primer linea
                next(info)
                # Recorre por todos los elementos
                for row in info:
                    self.cursor.execute(
                        f"""
                        INSERT INTO {nombre_tabla} (employee_id, department, performance_score, years_with_company, salary)
                        VALUES (%s, %s, %s, %s, %s)
                        """, 
                        (row[1], row[2], row[3], row[4], row[5]))
                        
                # Luego se confirman los datos ingresados en la bd
                self.conexion.commit()
                print("Datos insertados correctamente")
        except Exception as e:
            print(f"Error al insertar datos: {e}")


    # Se realiza la consulta a la base de datos con pandas
    def consulta(self, sql):
        try:
            df = pd.read_sql(sql, self.conexion)
            return df
        except Exception as e:
            print(f"Error al extraer datos: {e}")
            return None


# Clase para realizar los analisis de datos
class Analisis:

    def __init__(self, df):
        self.df = df

    def calcular_media(self, columna):
        return self.df[columna].mean()
    
    def calcular_mediana(self, columna):
        return self.df[columna].median()
    
    def calcular_desviacion_estandar(self, columna):
        return self.df[columna].std()


#     print("CÁLCULOS DEL SALARY")

#     print("MEDIA")
#     # Se calcula la media del salary
#     media_salary = df['salary'].mean()
#     print(media_salary)

#     print("MEDIANA")
#     # Se calcula la mediana del salary
#     mediana_salary = df['salary'].median()
#     print(mediana_salary)

#     print("DESVIACIÓN ESTÁNDAR")
#     # Se calcula la desviación estándar del salary
#     desviacion_estandar_salary = df['salary'].std()
#     print(desviacion_estandar_salary)

#     print("CANTIDAD DE EMPLEADOS POR DEPARTAMENTO")
#     # Se calcula el número de empleados por departamento
#     empleados_por_departamento = df.groupby('department')['employee_id'].count()
#     print(empleados_por_departamento)

#     print("CORRELACIÓN ENTRE YEARS_WITH_COMPANY Y PERFORMANCE_SCORE")
#     # Se calcula de correlacion entre YEARS_WITH_COMPANY Y PERFORMANCE_SCORE
#     correlacion_anios_y_performance = df['years_with_company'].corr(df['performance_score'])
#     print(correlacion_anios_y_performance)

#     print("CORRELACIÓN ENTRE SALARY Y PERFORMANCE SCORE")
#     # Se calcula de correlacion entre salary y performance score
#     correlacion_salary_y_performance = df['salary'].corr(df['performance_score'])
#     print(correlacion_salary_y_performance)

#     print("GRAFICO DE DISPERSION DE YEAR_WITH_COMPANY vs PERFORMANCE_SCORE")
#     # Gráfico de dispersión de years_with_company vs performance_score
#     plt.figure()
#     plt.scatter(df['years_with_company'], df['performance_score'], alpha=0.7)
#     plt.title('Years with Company vs Performance Score')
#     plt.xlabel('Years with Company')
#     plt.ylabel('Performance Score')
#     plt.show()

#     print("GRAFICO DE DISPERSION DE SALARY vs PERFORMANCE_SCORE")
#     # Gráfico de dispersión de salary vs performance_score
#     plt.figure()
#     plt.scatter(df['salary'], df['performance_score'], alpha=0.7)
#     plt.title('Salary vs Performance Score')
#     plt.xlabel('Salary')
#     plt.ylabel('Performance Score')
#     plt.show()

# except Exception as e:
#     print(f"Error al extraer datos: {e}")


# Realizar la conexion a la base de datos
db_connection = ConexionDB(host="localhost", user="root", password="")
db_connection.conectar()

# Para crea la base de data y la tabla
db_connection.crear_db("CompanyData")
db_connection.usar_db("CompanyData")

consulta_crear_tabla = """
        CREATE TABLE IF NOT EXISTS EmployeePerformance (
            id INT PRIMARY KEY AUTO_INCREMENT,
            employee_id INT,
            department VARCHAR(40),
            performance_score FLOAT,
            years_with_company INT,
            salary FLOAT
        )
    """

db_connection.crear_tabla(consulta_crear_tabla)

# Para insertar los datos desde el archivo
db_connection.insertar_datos("EmployeePerformance", "EmployeePerformance.csv")

# Para realiza la consulta a la base de datos
df = db_connection.consulta("SELECT * FROM EmployeePerformance")

if(df is not None):

    analitica = Analisis(df)


    # Se calcula la media del performance_score
    print("CÁLCULOS DEL PERFORMANCE SCORE")
    print("MEDIA")
    media_performance_score = analitica.calcular_media("performance_score")
    print(media_performance_score)

    print("MEDIANA")
    # Se calcula la mediana del performance_score
    mediana_performance_score = analitica.calcular_mediana("performance_score")
    print(mediana_performance_score)

    print("DESVIACIÓN ESTÁNDAR")
    # Se calcula la desviación estándar del performance_score
    desviacion_estandar_performance_score = analitica.calcular_desviacion_estandar("performance_score")
    print(desviacion_estandar_performance_score)

