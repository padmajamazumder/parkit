# Use Alpine-based Python image
FROM python:3.9.23-alpine3.22

RUN apk update && apk add --no-cache nodejs npm

RUN pip install --upgrade pip

WORKDIR /usr/src/app

COPY backend/ ./backend/
COPY frontend/ ./frontend/

WORKDIR /usr/src/app/frontend
RUN npm install
RUN npm run build

WORKDIR /usr/src/app/backend
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
