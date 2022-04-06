import psycopg2

hostname = 'localhost'
database  = 'database_1'
#username = 'postgres'
username = 'escuela_user'
#pwd = 'panasonicavg5'
pwd = 'en5570346521'
port_id = 5432
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
    insert_value = [(1, 'Jammy', 'B', 96.0, "3", False),(2, 'JJ', 'D', 97.5, "2", False)]
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
