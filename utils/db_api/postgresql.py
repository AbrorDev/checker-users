import sqlite3

class Database:

    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id INT SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        deep_link BIGINT NULL,
        count INT NOT NULL
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, username, telegram_id, deep_link, count = 0):
        sql = "INSERT INTO users (username, telegram_id, deep_link, count) VALUES($1, $2, $3, $4)"
        return self.execute(sql, parameters=(username, telegram_id, deep_link, count), commit=True)

    async def check_user(self, id):
        sql = f"SELECT COUNT(*) FROM Users WHERE telegram_id={id}"
        count = self.execute(sql, fetchone=True)
        return count[0] == 1
    
    async def check_fullname(self, id):
        sql = f"SELECT full_name FROM Users WHERE telegram_id={id}"
        count = self.execute(sql, fetchone=True)
        print(count)
        return count != None

    async def select_all_users(self):
        sql = "SELECT * FROM Users ORDER BY count"
        return self.execute(sql, fetchall=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM Users WHERE telegram_id = {telegram_id}"
        return self.execute(sql, fetchone=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return self.execute(sql, fetchone=True)
    
    async def get_gt_count(self,count):
        sql = f"SELECT * FROM Users WHERE count >= {count} ORDER BY count"
        return self.execute(sql, fetchall=True)

    async def update_user_fullname(self, fullname, telegram_id):
        sql = "UPDATE Users SET full_name=$1 WHERE telegram_id=$2"
        return self.execute(sql, parameters=(fullname, telegram_id), commit=True)
    
    async def update_count(self, telegram_id):
        number = await self.select_user(telegram_id)
        count = int(number[-1]) + 1
        sql = "UPDATE Users SET count=$1 WHERE telegram_id=$2"
        return self.execute(sql, parameters=(str(count), telegram_id), commit=True)

    async def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    async def delete_user(self, telegram_id):
        self.execute(f"DELETE FROM Users WHERE telegram_id={telegram_id}", commit=True)

    async def drop_users(self):
        self.execute("DROP TABLE Users", commit=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")