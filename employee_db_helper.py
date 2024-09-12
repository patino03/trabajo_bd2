import os
import mysql.connector
from mysql.connector import Error

def insert_employee_data(df, table_name='employee_table'):
    """Inserta datos en la base de datos"""
    connection = None
    cursor = None

    try:
        
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT"))  
        )

        if connection.is_connected():
            cursor = connection.cursor()

            
            insert_query = f"""
            INSERT INTO {table_name} (ID, Age, Income, Expenses, Weekly_Hours)
            VALUES (%s, %s, %s, %s, %s)
            """

            
            employee_data = df.to_records(index=False).tolist()

            
            cursor.executemany(insert_query, employee_data)
            
            
            connection.commit()

            print(f"{cursor.rowcount} rows inserted successfully.")

    except Error as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
