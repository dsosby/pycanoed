import os

DATABASE_URL=os.environ.get('MONGOHQ_URL', os.environ.get('DATABASE_URL'))
DEBUG=(os.environ.get('DEBUG', '').lower() == "true")
SECRET_KEY=os.environ.get('SECRET_KEY', '')
VALID_PASSWORD=os.environ.get('VALID_PASSWORD')
