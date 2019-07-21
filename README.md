# Work at Olist ##

## Testing ##
Running the tests needs to install the `requirements-dev.txt`
```
pip install -r requirements-dev.txt
```
Command for running:
```
pytest -v
```

## Environment Variables ##
```
DATABASE_URL=postgresql://user:pass@host:port/database_name
# postgresql://postgres:mysenha1sfoda@localhost:5432/postgres
```

## Migration ##
Uses alembic for database migration. If the environment variable DATABASE_URL is defined, the script connects in there, 
else it uses the database url is defined in the file: `alembic.ini`
  
Creating a new revision:  
`alembic revision -m "my_new_revision" --autogenerate`
  
Running migrations to head:  
`alembic upgrade head`  
  
Running migrations to previous revision:  
`alembic downgrade -1`  

## Running ##
Create a virtualenv, activate it and install the requirements:  
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```  
Run the app.py  
```
python app.py
```  

## Deploy to Heroku ##
The deploy is done directly from the Heroku app connect to my repository  
https://workatolist-lvs.herokuapp.com

## Work Environment ##
1. SO: macOS 10.14.5  
1. IDE: Pycharm Professional 2019.1.3  
1. Libs:  
3.1. Bottle: Web Framework  
3.2. Sqlalchemy: ORM  
3.3. Marshmallow: Serialization  
3.4. Alembic: Database migration  
3.5. Pytest: Unit tests  
3.6. WebTest: HTTP tests