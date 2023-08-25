import psycopg2
import db_config

conn = psycopg2.connect(database=db_config.DATABASE_NAME,
                        host=db_config.HOST,
                        user=db_config.USER,
                        password=db_config.PASSWORD,
                        port=db_config.PORT)



if __name__ == '__main__':
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())