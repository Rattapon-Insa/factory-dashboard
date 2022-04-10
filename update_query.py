from ast import While
import psycopg2
import time

hostname = 'localhost'
database  = 'database_1'
# username = 'postgres'
username = 'escuela_user'
# pwd = 'panasonicavg5'
pwd = 'en5570346521'
port_id = 5432
conn = None
cur = None

class query_check:
    def fetch():
        try:
            conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id
            )

            cur = conn.cursor()
            insert_script = 'SELECT * FROM robot '
            cur.execute(insert_script)
            result = cur.fetchall()
            conn.commit()

        except Exception as error:
            print(error)

        finally:
            if cur is not None:
                cur.close
            if conn is not None:
                conn.close()
        return result

    def update(pos,status, battery, name):
        try:
            conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id
            )

            cur = conn.cursor()

            insert_script = 'UPDATE robot SET position = %s, status = %s, battery = %s WHERE name = %s'
            insert_value = [(pos, status, battery, name)]
            for record in insert_value:
                cur.execute(insert_script, record)
            conn.commit()

        except Exception as error:
            print(error)

        finally:
            if cur is not None:
                cur.close
            if conn is not None:
                conn.close()   
    
    def update_status(status, name):
        try:
            conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id
            )

            cur = conn.cursor()

            insert_script = 'UPDATE robot SET status = %s WHERE name = %s'
            insert_value = [(status, name)]
            for record in insert_value:
                cur.execute(insert_script, record)
            conn.commit()

        except Exception as error:
            print(error)

        finally:
            if cur is not None:
                cur.close
            if conn is not None:
                conn.close()  

    def check_status():
        query = query_check.fetch()
        if query[1][1] == "Robot-X":
            R_X = query[1]
            R_y = query[0]
        else:
            R_X = query[0]
            R_y = query[1]
        return R_X, R_y
