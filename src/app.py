from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

@app.get('/') #@app.get('\'): This is called a decorator. It tells Python, when someone visits this URL,
              # run the following function.
def home():
    return {

        'message' : 'Welcome to RoadSense API!'
    }

@app.get('/hello')
def say_hellp():
    return {

        'message' : 'Hello, RoadSense!'
    }

@app.get('/accidents/{accident_id}')
def get_accident(accident_id: int):  #Why int? It is a type hint and FastAPI uses it to 
                                     #vaidate user input autometicallyl.

    return {
        'accident_id': accident_id
    }

@app.get('/search')
def search(severity: str):
    return {
        'severity': severity
    }

@app.post('/accidents')
def create_accident(data: dict = Body(...)):
    return {
        'received': data
    }