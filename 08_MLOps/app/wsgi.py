"""
Dieses Modul stellt ein Web Server Gateway Interface bereit, dass 
eine Swagger API bereitstellt, um das Modell aufzurufen.
Ausführung im Entwicklungsmodus:
```
python wsgi.py
```
"""

from fastapi import FastAPI

from pydantic import BaseModel, Field

import joblib
import pandas as pd

# Erzeugen der Flask WSGI Anwendung
app = FastAPI()

# Modell laden
clf = joblib.load("models/model.pkl")

# Im folgenden Code werden die Ein- und Ausgabefelder exakt 
# für die Swagger API definiert. Dieser Code muss jeweils auf 
# das Problem angepasst werden.

# Datenmodell der Eingabe
class Iris(BaseModel):

    sepal_length: float = Field(alias="sepal length (cm)", description="sepal length (cm)", example=2.4)
    sepal_width: float = Field(alias="sepal width (cm)", description="sepal width (cm)", example=2.4)
    petal_length: float = Field(alias="petal length (cm)", description="petal length (cm)", example=2.4)
    petal_width: float = Field(alias="petal width (cm)", description="petal width (cm)", example=2.4)


# Datenmodell der Ausgabe
class Response(BaseModel):
    pred: str = Field(description="Prediction", example="versicolor")

# Dieser Code definiert die Schnittstelle zum Modell
# und wird über die Route /v1 aufgerufen.
@app.post('/predict')
async def predict(iris: Iris):
        # Hier ggf. das JSON Eingabe-Objekt in den vom Modell
        # erwarteten Datentyp ändern.
        df = pd.DataFrame.from_dict([iris.dict(by_alias=True)])
        return Response(pred=clf.predict(df)[0])

@app.get('/healthcheck')
async def healthcheck():
    return {"status": "ok"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)