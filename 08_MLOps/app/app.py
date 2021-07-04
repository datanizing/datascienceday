from fastapi import FastAPI, Response
from pydantic import BaseModel, Field
from transformers import pipeline
import yaml

from .monitoring import instrumentator


# Erzeugen der FastAPI Anwendung
app = FastAPI(
    title="Sentiment Model API",
    description="Sentiment Model API",
    version="0.1",)

# Prometheus Instrumentator verknüpfen
instrumentator.instrument(app).expose(app, include_in_schema=True, should_gzip=True)

# Modell laden
model_path = "models/model"
sentiment_classifier = pipeline("sentiment-analysis", model_path)

with open("models/model.dvc", "r") as f:
    model_md5 = yaml.load(f, Loader=yaml.FullLoader)["outs"][0]["md5"]

# Datenmodell der Eingabe
class Input(BaseModel):
    sentence: str = Field(example="Das ist ein toller Satz.")

# Datenmodell der Ausgabe
class Sentiment(BaseModel):
    label: str = Field(description="Sentiment", example="NEGATIVE")
    score: float = Field(description="Score", example=0.9526780247688293)

# Dieser Code definiert die Schnittstelle zum Modell
# und wird über die Route /predict aufgerufen.
@app.post('/predict', response_model=Sentiment, operation_id="predict_post")
async def predict(response: Response, input: Input):
        pred=sentiment_classifier(input.sentence)[0]
        sentiment = Sentiment.parse_obj(pred)
        response.headers["X-model-score"] = str(sentiment.score)
        response.headers["X-model-sentiment"] = str(sentiment.label)
        response.headers["X-model-hash"] = model_md5
        return sentiment

@app.get('/healthcheck')
async def healthcheck():
    return {"status": "ok"}

if __name__ == '__main__':
    # Webserver starten, wenn Modul ausgeführt wird
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)