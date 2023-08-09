import pymysql
import db_config

class DatabaseManager:
    def  __init__(self):
        self.connection = pymysql.connect(host=db_config.host,
                user=db_config.user,
                password=db_config.password,
                database=db_config.database)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        self.connection.commit()
        return result

    def execute_update(self, query, params=None):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()
        
    def execute_insert(self, insert_sql: str, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(insert_sql, params)
            result  = cursor.fetchall()
        self.connection.commit()
        return result
    
    def remove_duplicate_rows(self):
        try:
            with self.connection.cursor() as cursor:
                # 构建 SQL 查询，选择每个用户名的最小 ID
                select_query = """
                    SELECT MIN(ID) AS min_id, username
                    FROM users
                    GROUP BY username
                """
                cursor.execute(select_query)
                results = cursor.fetchall()
                delete_query = """
                    DELETE FROM users
                    WHERE ID NOT IN ({})
                """.format(','.join(str(result['min_id']) for result in results))
                cursor.execute(delete_query)
                self.connection.commit()
                print("Duplicate rows removed successfully.")
        except Exception as e:
            print("An error occurred:", e)
