FROM python:3.12

# Set the working directory in the container
WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r ./requirements.txt
# RUN python manage.py makemigrations 
# RUN python manage.py migrate
# RUN python manage.py create_superuser
# Expose the port on which the Django app will run
EXPOSE 8000

# Run the Django app
CMD ["gunicorn", "studybud.asgi:application", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]