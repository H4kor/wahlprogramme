FROM python:3.10

# Expose ports
EXPOSE 8000

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "wsgi:app"]