# Uvicorn will run FastAPI on port 8080 for OpenShift
FROM registry.access.redhat.com/ubi8/python-39

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
