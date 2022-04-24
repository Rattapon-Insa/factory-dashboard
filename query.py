import psycopg2

hostname = 'localhost' # need to change later
database  = 'database_1'
username = 'escuela_user' # need to postgres 
pwd = 'en5570346521' # need to change to panasonicavg5
port_id = 5432 # need to change to 5433
conn = None
cur = None


try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )

    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS robot')

    create_script = """CREATE TABLE IF NOT EXISTS robot (
        id int PRIMARY KEY,
        name varchar(40) NOT NULL,
        position varchar(40),
        battery float4,
        status varchar(40),
        callback boolean
    )
    """

    cur.execute(create_script)

    insert_script = 'INSERT INTO robot (id, name, position, battery, status, callback) VALUES ( %s,%s, %s, %s, %s, %s)'
    insert_value = [(1, 'Robot-X', 'E', 96.0, "3", False),(2, 'Robot-Y', 'F', 97.5, "1", False)]
    for record in insert_value:
        cur.execute(insert_script, record)
    cur.execute('SELECT * FROM robot')
    print(cur.fetchall())
 
 
    conn.commit()

except Exception as error:
    print(error)

finally:
    if cur is not None:
        cur.close
    if conn is not None:
        conn.close()   
