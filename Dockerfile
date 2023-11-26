FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV ENV=prod 
ENV TZ=Asia/Kolkata
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .