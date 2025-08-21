FROM python:3.14.0rc2-alpine3.22

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY python_job_scheduler.py ./

# Run the binary
CMD ["python", "/app/python_job_scheduler.py"]
