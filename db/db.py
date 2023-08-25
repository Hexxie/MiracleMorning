import psycopg2
from .db_config import DATABASE_NAME, HOST, USER, PASSWORD, PORT

conn = psycopg2.connect(database=DATABASE_NAME,
                        host=HOST,
                        user=USER,
                        password=PASSWORD,
                        port=PORT)

def find_user_by_tg_id(tg_id: int) -> int:
    """ Searches user by it's telegram id

        Parameters
        ----------
        tg_id : int
            telegram id of the user received from update
        Raises
        ------
            none.
        Returns
        ------
            user id from database or -1 if user not found
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE telegram_id = {str(tg_id)}")
    data = cursor.fetchall()
    cursor.close()
    print("data")
    print(data)
    return -1 if not data else data[0][0]

def add_user(name: str, gender: int, tg_id: int) -> bool:
    """ Searches user by it's telegram id

        Parameters
        ----------
        name : str
            user's real name
        gender : int
            0 - man or unknown
            1 - woman
        tg_id : int
            telegram id
        Raises
        ------
            psycopg2.errors.UniqueViolation:
                If telegram id already exists
        Returns
        ------
            true if user was added 
    """
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute(f"INSERT INTO users (first_name, gender, telegram_id) VALUES ('{name}', {str(gender)}, {str(tg_id)})")
        conn.commit()
        success = True
    except psycopg2.errors.UniqueViolation:
        #TODO put this into logs
        print("telegram id already exists")
        cursor.execute("rollback")
        
    
    cursor.close()
    return success



if __name__ == '__main__':
    print(find_user_by_tg_id(1))
    add_user("generated", 0, 123)
    print(find_user_by_tg_id(123))

#TODO you have to create a class here with cursor.close() or rollback