-- Create workout_sessions table
CREATE TABLE IF NOT EXISTS workout_sessions (
    id SERIAL PRIMARY KEY,
    session_date DATE NOT NULL DEFAULT CURRENT_DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create exercises table with foreign key to workout_sessions
CREATE TABLE IF NOT EXISTS exercises (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES workout_sessions(id) ON DELETE CASCADE,
    exercise_name VARCHAR(100) NOT NULL,
    reps INTEGER NOT NULL CHECK (reps > 0),
    sets INTEGER NOT NULL CHECK (sets > 0),
    pounds DECIMAL(10, 2) NOT NULL CHECK (pounds > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for optimized queries
CREATE INDEX IF NOT EXISTS idx_workout_sessions_date ON workout_sessions(session_date);
CREATE INDEX IF NOT EXISTS idx_exercises_session_id ON exercises(session_id);
CREATE INDEX IF NOT EXISTS idx_exercise_name ON exercises(exercise_name);