from turtle import position
import matplotlib.pyplot as plt
import cv2
import numpy as np
import streamlit as st
import psycopg2
from streamlit_autorefresh import st_autorefresh

def main():
    # update every 15 second
    st_autorefresh(interval= 1 * 1000, key="queryrefresh")


    def init_connection():
        return psycopg2.connect(**st.secrets["postgres"])

    conn = init_connection()
    cur = conn.cursor()

    # Perform query.
    # Uses st.cache to only rerun when the query changes or after 10 min.
    def run_query(query):
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    # header area
    st.title('Robot dashboard')
    st.write('This is dashboard for robot')

    dict_robot = {'robot A':
                    {
                        'name':"",
                        'position': 0,
                        'battery' : 0.0,
                        'status': 0,
                        'callback' : False
                    },
                    'robot B' :{
                        'name':"",
                        'position': 0,
                        'battery' : 0.0,
                        'status': 0,
                        'callback' : False
                    }
    }


    # sidebar area
    st.sidebar.write("Robot control section:")
    if st.sidebar.button('Robot X, call back'):
        update_script = 'UPDATE robot SET callback = true WHERE id = 1;'
        cur.execute(update_script)

    if st.sidebar.button('Robot Y, call back'):
        update_script = 'UPDATE robot SET callback = true WHERE id = 2;'
        cur.execute(update_script)


    rows = run_query("SELECT * from robot;")

    conn.close()

    positon_dict = {
        'standby':{"x": 396,"y": 812.8},
        'I': {"x": 573.7, "y": 815.1},
        'A':{'x': 756.1, 'y': 735.9},
        'B':{'x': 1067.3, 'y': 813.5},
        'C':{'x': 1245.7, 'y': 520.2},
        'D':{'x': 839.1, 'y': 239.3},
        'F':{'x': 670.0, 'y': 126.8},
        'G':{'x': 1179.8, 'y': 127.6},
        'H':{'x': 1339.6, 'y': 285.1}
    }

    status_dict = {
        "1" : 'Go',
        "2" : 'Wait',
        "3" : 'standby'
    }

    # assign query result to dictionary
    for row in rows:
        if row[0] == 1:
            dict_robot['robot A']['name'] = row[1]
            dict_robot['robot A']['position'] = row[2]
            dict_robot['robot A']['battery'] = row[3]
            dict_robot['robot A']['status'] = row[4]
            dict_robot['robot A']['callback'] = row[5]
        else:
            dict_robot['robot B']['name'] = row[1]
            dict_robot['robot B']['position'] = row[2]
            dict_robot['robot B']['battery'] = row[3]
            dict_robot['robot B']['status'] = row[4]
            dict_robot['robot B']['callback'] = row[5]




    col1, col2, col3 = st.columns(3)
    col1.metric("Robot A position", str( dict_robot['robot A']['position']))
    col2.metric("Battery", str( dict_robot['robot A']['battery'])+"%")
    col3.metric("status",str(status_dict[dict_robot['robot A']['status']]))

    col1.metric("Robot B position", str( dict_robot['robot B']['position']))
    col2.metric("Battery", str( dict_robot['robot B']['battery'])+"%")
    col3.metric("status",str(status_dict[dict_robot['robot B']['status']]))

    #initial position and size
    position1_x = int(positon_dict[dict_robot['robot A']['position']]['x'])
    position1_y = int(positon_dict[dict_robot['robot A']['position']]['y'])
    position2_x = int(positon_dict[dict_robot['robot B']['position']]['x'])
    position2_y = int(positon_dict[dict_robot['robot B']['position']]['y'])
    size = 18

    # graph area
    image = cv2.imread("Main_dashboard.png", cv2.IMREAD_COLOR)
    # Draw a rectangle (thickness is a positive integer)
    imageRectangle = image.copy()
    imageRectangle = cv2.cvtColor(imageRectangle, cv2.COLOR_BGR2RGB)
    # render position
    cv2.circle(imageRectangle, (position1_x,position1_y), size,(0,0,255),-1);
    cv2.circle(imageRectangle, (position2_x,position2_y), size,(0,255,255),-1);

    fig, ax = plt.subplots(); ax.imshow(imageRectangle); ax.axis('off')
    chart = st.pyplot(fig)
    print('done query executed')

if __name__ == '__main__':
    main()