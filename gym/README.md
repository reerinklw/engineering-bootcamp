# Gym Tracking App

A simple gym tracking application built with Streamlit, PostgreSQL, and Docker. Log your workout sessions with multiple exercises and track your volume progress over time.

## Features

- **Session-based logging**: Create workout sessions and add multiple exercises per session
- **Volume tracking**: Track total volume (sets × reps × pounds) over time
- **Interactive charts**: Visualize progress with Plotly charts
- **Data persistence**: PostgreSQL database with Docker volume for data persistence
- **Simple interface**: Clean, intuitive Streamlit interface

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Data Visualization**: Plotly
- **Database Connector**: psycopg2

## Prerequisites

- Docker installed on your machine
- Docker Compose installed

## Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd gym
   ```

2. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Open your browser and navigate to: `http://localhost:8502`
   - The application will automatically initialize the database on first run

## Usage

### Log Workout
1. Navigate to the "Log Workout" page
2. Select the workout date and add optional notes
3. Specify the number of exercises you want to log
4. For each exercise, enter:
   - Exercise name (e.g., "Bench Press")
   - Reps (number of repetitions per set)
   - Sets (number of sets)
   - Pounds (weight lifted)
5. Click "Save Workout Session" to save your workout

### View Progress
1. Navigate to the "View Progress" page
2. Select specific exercises to filter the charts
3. View interactive charts showing:
   - Total daily volume over time
   - Volume progression by exercise
   - Total volume comparison by exercise

### Session History
1. Navigate to the "Session History" page
2. Browse all past workout sessions
3. Expand each session to see detailed exercise information

## Database Schema

### workout_sessions
- `id`: Primary key
- `session_date`: Date of the workout session
- `notes`: Optional notes about the session
- `created_at`: Timestamp when session was created

### exercises
- `id`: Primary key
- `session_id`: Foreign key to workout_sessions
- `exercise_name`: Name of the exercise
- `reps`: Number of repetitions per set
- `sets`: Number of sets
- `pounds`: Weight lifted in pounds
- `created_at`: Timestamp when exercise was logged

## Token Optimization Features

The application includes several optimizations to minimize computational overhead:

- **Connection pooling**: Reuses database connections
- **Streamlit caching**: Caches expensive database queries and data processing
- **Efficient database queries**: Optimized SQL with proper indexing
- **Lazy data loading**: Only fetches data when needed
- **Minimal dependencies**: Only essential packages included
- **Batch operations**: Uses transactions for multi-exercise inserts

## Stopping the Application

To stop the application:
```bash
docker-compose down
```

To stop and remove all data (including database):
```bash
docker-compose down -v
```

## Troubleshooting

### Application not loading
- Ensure Docker is running
- Check that ports 8501 and 5432 are not already in use
- Run `docker-compose logs` to check for errors

### Database connection issues
- Verify PostgreSQL container is healthy: `docker-compose ps`
- Check database credentials in docker-compose.yml
- Restart containers: `docker-compose restart`

### Data not persisting
- Ensure the postgres_data volume exists: `docker volume ls`
- Check volume permissions and disk space

## Customization

### Change database credentials
Edit the environment variables in `docker-compose.yml`:
```yaml
environment:
  POSTGRES_DB: your_database_name
  POSTGRES_USER: your_username
  POSTGRES_PASSWORD: your_password
```

### Add more exercises per session
Modify the `max_value` in the number_input in `streamlit_app.py`:
```python
exercise_count = st.number_input("Number of exercises", min_value=1, max_value=20, value=1)
```

## License

This project is open source and available for personal use.