"""
Dieses Modul stellt ein Web Server Gateway Interface bereit, dass 
eine Swagger API bereitstellt, um das Modell aufzurufen.
Ausführung im Entwicklungsmodus:
```
python wsgi.py
```
"""

from fastapi import FastAPI, Response
from pydantic import BaseModel, Field
from transformers import pipeline

from monitoring import instrumentator

# Erzeugen der Flask WSGI Anwendung
app = FastAPI()
instrumentator.instrument(app).expose(app, include_in_schema=True, should_gzip=True)
# Modell laden
sentiment_classifier = pipeline("sentiment-analysis", "models/model_v1")

# Im folgenden Code werden die Ein- und Ausgabefelder exakt 
# für die Swagger API definiert. Dieser Code muss jeweils auf 
# das Problem angepasst werden.

# Datenmodell der Eingabe
class Input(BaseModel):
    sentence: str = Field(example="Das ist ein toller Satz.")

# Datenmodell der Ausgabe
class Sentiment(BaseModel):
    label: str = Field(description="Sentiment", example="NEGATIVE")
    score: float = Field(description="Score", example=0.9526780247688293)

# Dieser Code definiert die Schnittstelle zum Modell
# und wird über die Route /v1 aufgerufen.
@app.post('/predict', response_model=Sentiment)
async def predict(response: Response, input: Input):
        # Hier ggf. das JSON Eingabe-Objekt in den vom Modell
        # erwarteten Datentyp ändern.
        pred=sentiment_classifier(input.sentence)[0]
        sentiment = Sentiment.parse_obj(pred)
        response.headers["X-model-score"] = str(sentiment.score)
        response.headers["X-model-sentiment"] = str(sentiment.label)
        return sentiment

@app.get('/healthcheck')
async def healthcheck():
    return {"status": "ok"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)