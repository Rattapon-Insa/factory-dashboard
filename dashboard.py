from turtle import position
import matplotlib.pyplot as plt
import cv2
import numpy as np
import streamlit as st
import psycopg2
from update_query import query_check
from streamlit_autorefresh import st_autorefresh

def main():
    # update every 15 second
    st_autorefresh(interval= 3 * 1000, key="queryrefresh")


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

    rows = run_query("SELECT * from robot;")

    conn.close()

    positon_dict = {
        'standby':{"x": 250,"y": 923},
        'F': {"x": 495, "y": 923},
        'D':{'x': 1075, 'y': 923},
        'E':{'x': 709, 'y': 830},
        'G':{'x': 1284, 'y': 579},
        'H':{'x': 1275, 'y': 214},
        'A':{'x': 1106, 'y': 215},
        'B':{'x': 1430, 'y': 242},
        'C':{'x': 1392, 'y': 580}
    }

    status_dict = {
        "1" : 'Go',
        "2" : 'Wait',
        "3" : 'standby'
    }

    # Call back function at sidebar
    if st.sidebar.button('Call Robot A back'):
        query_check.update_callback(True, 'Robot-X')
        print(query_check.fetch())
    else:
        print(query_check.fetch())

    if st.sidebar.button('Call Robot B back'):
        query_check.update_callback(True, 'Robot-Y')
        print(query_check.fetch())
    else:
        print(query_check.fetch())

    if st.sidebar.button('Reset call back'):
        query_check.update_callback(False, 'Robot-Y')
        query_check.update_callback(False, 'Robot-X')
        print(query_check.fetch())


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
    size = 25

    # graph area
    image = cv2.imread("Dashboard.png", cv2.IMREAD_COLOR)
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