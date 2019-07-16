# Work at Olist ##

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

## Migration ##
Uses alembic for database migration.  
  
Creating a new revision:  
`alembic revision -m "my_new_revision" --autogenerate`
  
Running migrations to head:  
`alembic upgrade head`  
  
Running migrations to previous revision:  
`alembic downgrade -1`  

