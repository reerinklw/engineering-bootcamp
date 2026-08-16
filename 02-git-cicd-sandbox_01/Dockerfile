FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/calculator/ ./apps/calculator/

EXPOSE 8501

CMD ["streamlit", "run", "apps/calculator/calculator_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
