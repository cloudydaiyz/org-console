FROM python:3.9.18-alpine

ENV APP_PORT=5001

WORKDIR /app

COPY . .

EXPOSE $APP_PORT

# RUN ["python", "-m", "pip", "install", "-r", "requirements.txt"]
RUN python -m pip install -r requirements.txt

# CMD ["python", "-m", "flask", "--app", "src/app", "--port", $PORT]
CMD python -m flask --app src/app run --port $APP_PORT --host 0.0.0.0