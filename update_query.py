from ast import While
import psycopg2
import time

hostname = 'localhost'
database  = 'database_1'
#username = 'postgres'
username = 'escuela_user'
#pwd = 'panasonicavg5'
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

    def stop_go(A, B, pos_a, pos_b, final_pos_b):
        if A[2] == pos_a and B[2] != pos_a:
            # if A in concern position, B is not in concern position
            print("start checking")
            name = A[1]
            status = '2'
            print('update status')
            query_check.update_status(status, name)
            print(query_check.fetch())
            print('{} wait for 5 seconds'.format(A[1]))
            time.sleep(5)
            print('Done waiting')
            query_check.update_status("1",name)
            print(query_check.fetch())
               
        elif A[2] == pos_a and B[2] == pos_b:
            # if A in concern position, B in concern position
            name_A = A[1]
            name_B = B[1]
            status = '2'
            # Check B status to stop
            query_check.update_status(status, name_A)
            print('{a} will start waiting until {b} reach target : {c}'.format(a = A[1], b = B[1], c = final_pos_b))
        else:
            print('Not following the defined cases')
    
    def check_logic_X(query):
        if query[1][1] == "Robot-X":
            R_X = query[1]
            R_y = query[0]
        else:
            R_X = query[0]
            R_y = query[1]
        print(R_X)
        print(R_y)
        print(R_X[2]," is the current postion of ", R_X[1])
        if R_X[2] == "A":
            A = R_X
            B = R_y              
            pos_a = "A"
            pos_b = 'C'
            final_pos_b = 'I'
            query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
        elif R_X[2] == "C":
            A = R_X
            B = R_y
            pos_a = "C"
            pos_b = 'A'
            final_pos_b = 'I'
            query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
        elif R_X[2] == "G":
            A = R_X
            B = R_y
            pos_a = "G"
            pos_b = 'H'
            final_pos_b = 'C'
            query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
        elif R_X[2] == "H":
            A = R_X
            B = R_y
            pos_a = "H"
            pos_b = 'G'
            final_pos_b = 'C'
            query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
        else:
            print('No condition met')

    def check_logic_Y(query):
        if query[1][1] == "Robot-Y":
            R_X = query[1]
            R_y = query[0]
        else:
            R_X = query[0]
            R_y = query[1]
        print(R_X)
        print(R_y)
        print(R_X[2]," is the current postion of ", R_X[1])
        if R_X[2] == "A":
            A = R_X
            B = R_y 
            pos_a = "A"
            pos_b = 'standby'
            final_pos_b = 'I'
            query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
        elif R_X[2] == "C":
            A = R_X
            B = R_y
            pos_a = "C"
            pos_b = 'standby'
            final_pos_b = 'I'
            query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
        elif R_X[2] == "G":
            A = R_X
            B = R_y
            pos_a = "G"
            pos_b = 'standby'
            final_pos_b = 'C'
            query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
        elif R_X[2] == "H":
            A = R_X
            B = R_y
            pos_a = "H"
            pos_b = 'standby'
            final_pos_b = 'C'
            query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
        else:
            print('No condition met')

            

                
