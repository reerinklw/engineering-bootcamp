import os
import psycopg2
from psycopg2 import pool
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import streamlit as st

# Database connection pool
@st.cache_resource
def get_connection_pool():
    return psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=5,
        host=os.getenv('DB_HOST', 'postgres'),
        database=os.getenv('DB_NAME', 'gym_tracker'),
        user=os.getenv('DB_USER', 'gym_user'),
        password=os.getenv('DB_PASSWORD', 'gym_password')
    )

def get_connection():
    return get_connection_pool().getconn()

def release_connection(conn):
    get_connection_pool().putconn(conn)

# Database operations
def init_database():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            with open('/app/init_db.sql', 'r') as f:
                cur.execute(f.read())
        conn.commit()
    except Exception as e:
        if "already exists" not in str(e):
            raise e
    finally:
        release_connection(conn)

@st.cache_data(ttl=300)
def get_all_sessions():
    conn = get_connection()
    try:
        query = """
        SELECT ws.id, ws.session_date, ws.notes, 
               COUNT(e.id) as exercise_count
        FROM workout_sessions ws
        LEFT JOIN exercises e ON ws.id = e.session_id
        GROUP BY ws.id, ws.session_date, ws.notes
        ORDER BY ws.session_date DESC
        """
        return pd.read_sql(query, conn)
    finally:
        release_connection(conn)

@st.cache_data(ttl=300)
def get_session_exercises(session_id):
    conn = get_connection()
    try:
        query = """
        SELECT id, exercise_name, reps, sets, pounds, 
               (sets * reps * pounds) as volume
        FROM exercises 
        WHERE session_id = %s
        ORDER BY id
        """
        return pd.read_sql(query, conn, params=(session_id,))
    finally:
        release_connection(conn)

@st.cache_data(ttl=300)
def get_volume_data():
    conn = get_connection()
    try:
        query = """
        SELECT ws.session_date, e.exercise_name, 
               (e.sets * e.reps * e.pounds) as volume
        FROM exercises e
        JOIN workout_sessions ws ON e.session_id = ws.id
        ORDER BY ws.session_date
        """
        return pd.read_sql(query, conn)
    finally:
        release_connection(conn)

@st.cache_data(ttl=300)
def get_exercise_list():
    conn = get_connection()
    try:
        query = "SELECT DISTINCT exercise_name FROM exercises ORDER BY exercise_name"
        df = pd.read_sql(query, conn)
        return df['exercise_name'].tolist()
    finally:
        release_connection(conn)

def create_workout_session(session_date, notes):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO workout_sessions (session_date, notes) VALUES (%s, %s) RETURNING id",
                (session_date, notes)
            )
            session_id = cur.fetchone()[0]
        conn.commit()
        return session_id
    finally:
        release_connection(conn)

def add_exercises_to_session(session_id, exercises):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for exercise in exercises:
                cur.execute(
                    "INSERT INTO exercises (session_id, exercise_name, reps, sets, pounds) VALUES (%s, %s, %s, %s, %s)",
                    (session_id, exercise['name'], exercise['reps'], exercise['sets'], exercise['pounds'])
                )
        conn.commit()
    finally:
        release_connection(conn)

# Initialize database
try:
    init_database()
except Exception as e:
    st.error(f"Database initialization error: {e}")

st.title("Gym Tracker")
st.sidebar.title("Navigation")

page = st.sidebar.radio("Select Page", ["Log Workout", "View Progress", "Session History"])

if page == "Log Workout":
    st.header("Log New Workout Session")
    
    col1, col2 = st.columns(2)
    with col1:
        session_date = st.date_input("Workout Date", date.today())
    with col2:
        notes = st.text_input("Notes (optional)")
    
    st.subheader("Exercises")
    exercises = []
    
    exercise_container = st.container()
    
    with exercise_container:
        exercise_count = st.number_input("Number of exercises", min_value=1, max_value=20, value=1)
        
        for i in range(exercise_count):
            st.write(f"Exercise {i+1}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                name = st.text_input(f"Exercise Name", key=f"name_{i}")
            with col2:
                reps = st.number_input(f"Reps", min_value=1, value=10, key=f"reps_{i}")
            with col3:
                sets = st.number_input(f"Sets", min_value=1, value=3, key=f"sets_{i}")
            with col4:
                pounds = st.number_input(f"Pounds", min_value=0.0, value=135.0, key=f"pounds_{i}")
            
            if name and reps > 0 and sets > 0 and pounds >= 0:
                exercises.append({
                    'name': name,
                    'reps': reps,
                    'sets': sets,
                    'pounds': pounds
                })
    
    if st.button("Save Workout Session") and exercises:
        try:
            session_id = create_workout_session(session_date, notes)
            add_exercises_to_session(session_id, exercises)
            st.success(f"Workout session saved with {len(exercises)} exercises!")
            st.cache_data.clear()
        except Exception as e:
            st.error(f"Error saving workout: {e}")

elif page == "View Progress":
    st.header("Volume Progress Tracking")
    
    volume_data = get_volume_data()
    
    if not volume_data.empty:
        exercise_list = get_exercise_list()
        selected_exercises = st.multiselect("Select Exercises", exercise_list, default=exercise_list[:5])
        
        if selected_exercises:
            filtered_data = volume_data[volume_data['exercise_name'].isin(selected_exercises)]
            
            # Total volume over time
            daily_volume = filtered_data.groupby('session_date')['volume'].sum().reset_index()
            fig1 = px.line(daily_volume, x='session_date', y='volume', 
                          title='Total Daily Volume',
                          labels={'volume': 'Volume (lbs × reps × sets)', 'session_date': 'Date'})
            st.plotly_chart(fig1, use_container_width=True)
            
            # Volume by exercise over time
            exercise_volume = filtered_data.groupby(['session_date', 'exercise_name'])['volume'].sum().reset_index()
            fig2 = px.line(exercise_volume, x='session_date', y='volume', color='exercise_name',
                          title='Volume Progression by Exercise',
                          labels={'volume': 'Volume (lbs × reps × sets)', 'session_date': 'Date'})
            st.plotly_chart(fig2, use_container_width=True)
            
            # Volume comparison by exercise
            total_by_exercise = filtered_data.groupby('exercise_name')['volume'].sum().reset_index()
            fig3 = px.bar(total_by_exercise, x='exercise_name', y='volume',
                         title='Total Volume by Exercise',
                         labels={'volume': 'Total Volume', 'exercise_name': 'Exercise'})
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No workout data available. Start logging workouts to see progress!")

elif page == "Session History":
    st.header("Workout Session History")
    
    sessions = get_all_sessions()
    
    if not sessions.empty:
        for _, session in sessions.iterrows():
            with st.expander(f"{session['session_date']} - {session['exercise_count']} exercises"):
                if session['notes']:
                    st.write(f"Notes: {session['notes']}")
                
                exercises = get_session_exercises(session['id'])
                if not exercises.empty:
                    exercises['volume'] = exercises['volume'].round(2)
                    st.dataframe(exercises[['exercise_name', 'reps', 'sets', 'pounds', 'volume']], 
                                hide_index=True)
    else:
        st.info("No workout sessions logged yet.")