# webapp

some useful instructions

## start 
1. create virtual environment
2. activate virtual environment
3. install pip dependencies
```
pip install -r requirements.txt
```
4. install dependencies in frontend folder
```
cd frontend
npm install
```
5. make migrations and etc.
```
python manage.py makemigrations
python manage.py migrate
```
## to run backend and frontend separately
backend runs on port 8000, frontend (development) on port 3000.

to run them separately just run the server from the `webapp` folder
```
python manage.py runserver
```
and run the client from the `frontend` folder
```
cd frontend
npm start
``` 

## to run backend and frontend together
to make everything run on port 8000

    cd frontend
    npm run build
    cd ..
    python manage.py runserver

### complaints

i assume full responsability of the poor code quality. if anything does not work feel free to complain at giacomo.lombardo@estudiantat.upc.edu 

