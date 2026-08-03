from fastapi import FastAPI
from fastapi import Body
from src.services.accident_service import AccidentService


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


service = AccidentService()

@app.get('/statistics')
def statistics():

    total = service.get_total_accidents()
    severe = service.get_severe_accident()
    peak_hour = service.get_peak_hour()
    hotspot = service.get_top_hotspot()


    return {
        'success': True,
        'data': {
            'total_accident': total,
            'severe_accidents': severe,
            'peak_hour': {
                'hour': peak_hour[0],
                'accidents': peak_hour[1]
            },

            'top_hotspot': {
                'location': hotspot[0],
                'accidents': hotspot[1]
            }
        }
    }

