FROM python:3.12-slim

WORKDIR /EasyConfig
COPY requirements.txt /EasyConfig/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /EasyConfig/

EXPOSE 8000

CMD ["python", "manage.py", "runserver","localhost:8080"]
