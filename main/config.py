import mysql.connector

def conectar_db():
    return mysql.connector.connect(host="localhost",
                                    user="root",
                                    passwd="",
                                    database="bd_pjd",
                                    charset="utf8mb4",
                                    collation="utf8mb4_general_ci")