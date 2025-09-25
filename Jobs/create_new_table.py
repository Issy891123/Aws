# create_new_table.py
import os
import mysql.connector
from mysql.connector import errorcode

def create_table():
    try:
        print("Conectando a la base de datos RDS...")
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME')
        )
        cursor = conn.cursor()
        
        table_name = "website_visits"
        print(f"Intentando crear la tabla '{table_name}' si no existe...")
        
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            visit_id INT AUTO_INCREMENT PRIMARY KEY,
            visitor_ip VARCHAR(45) NOT NULL,
            visit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_query)
        print(f"¡Tabla '{table_name}' creada o ya existente!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    create_table()