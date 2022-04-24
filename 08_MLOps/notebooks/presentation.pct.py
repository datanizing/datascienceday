# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python [conda env:mlops]
#     language: python
#     name: conda-env-mlops-py
# ---

# %% [markdown] slideshow={"slide_type": "slide"}
# # MLOps
#
# ![MLOps](https://nuernberg.digital/uploads/tx_seminars/praesentation2.jpg)

# %% [markdown] slideshow={"slide_type": "slide"}
# ![hidden technical debt paper](../images/hidden_technical_debt_2015.jpg)

# %% [markdown] slideshow={"slide_type": "subslide"}
# * __Reproduzierbarkeit__: 
#     * Versionierung von Daten und Code
# * __Experiment Tracking__:
#     * Dokumentation der Auswahl des Modells.
#     * Evaluation des Modells.
# * __Monitoring__:
#     * Überwachung des Verhaltens des Modells in Produktion

# %% [markdown] slideshow={"slide_type": "slide"}
# # Reproduzierbarkeit mit DVC
#
# [DVC](https://dvc.org/)
# ![DVC](../images/data_code_versioning.png)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## DVC Data
#
# [DVC Remote with Minio](http://localhost:9000/minio/titanic/)

# %% slideshow={"slide_type": "fragment"}
# ! cd .. & dvc push

# %% slideshow={"slide_type": "fragment"}
# ! cd .. & dvc pull

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Pipelines
# In DVC lassen sich Pipelines definieren und damit lasse sich Trainings-Skripte und Daten miteinander verbinden.
#
# ```yaml
# stages:
#   train:
#     cmd: python train.py
#     outs:
#     - ../models/model/
# ```

# %% [markdown] slideshow={"slide_type": "fragment"}
# Reproduzieren der Schritte mit
#
# ```bash
# dvc repro
# ```

# %% [markdown] slideshow={"slide_type": "slide"}
# # Sentiment API
#
# Mittels [FastAPI](https://fastapi.tiangolo.com/) wird eine API für das Model bereitgestellt.

# %% [markdown] slideshow={"slide_type": "subslide"}
# ### Datenmodell für Ein- und Ausgabe
#
# ```python
# from pydantic import BaseModel, Field
#
# # Datenmodell der Eingabe
# class Input(BaseModel):
#     sentence: str = Field(example="Das ist ein toller Satz.")
#
# # Datenmodell der Ausgabe
# class Sentiment(BaseModel):
#     label: str = Field(description="Sentiment", example="NEGATIVE")
#     score: float = Field(description="Score", example=0.9526780247688293)
# ```

# %% [markdown] slideshow={"slide_type": "subslide"}
# ### API Endpunkt
#
# ```python
# from fastapi import FastAPI, Response
#
# # Erzeugen der FastAPI Anwendung
# app = FastAPI(
#     title="Sentiment Model API",
#     description="Sentiment Model API",
#     version="0.1",)
#
# # Modell laden
# model_path = "models/model"
#
# @app.post('/predict', response_model=Sentiment, operation_id="predict_post")
# async def predict(response: Response, input: Input):
#         pred=sentiment_classifier(input.sentence)[0]
#         sentiment = Sentiment.parse_obj(pred)
#         return sentiment
# ```
#

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## API Testen
#
# [uvicorn Webserver](https://www.uvicorn.org/)
#
# ```python
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8080)
# ```
#
# Webserver starten
# ```
# python app.py
# ```

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Schnittstelle
#
# FastAPI stellt eine Dokumentation der Schnittstelle unter [/docs](http://localhost:8080/docs) zur Verfügung.

# %% [markdown] slideshow={"slide_type": "subslide"}
# ### Client Code erzeugen
# Der Client wird mittles [`openapi-python-client` Generator](https://github.com/openapi-generators/openapi-python-client) z.B. wie folgt erzeugt.
# ```
# openapi-python-client generate --url http://127.0.0.1/openapi.json
# ```

# %% [markdown] slideshow={"slide_type": "slide"}
# ## API Nutzen
# Vorbereitete Daten werden eingelesen

# %% slideshow={"slide_type": "skip"}
import pandas as pd
import numpy as np
import sqlite3
import sys

# %% slideshow={"slide_type": "fragment"}
data_df = pd.read_csv("../data/raw/transport-short.csv", header=None, nrows=1000, names=['id', 'kind', 'title', 'link_id', 'parent_id', 'ups', 'downs', 'score',
       'author', 'num_comments', 'created_utc', 'permalink', 'url', 'text',
       'level', 'top_parent'])

# %% slideshow={"slide_type": "-"}
data_df.head(2)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## API aufrufen

# %% slideshow={"slide_type": "fragment"}
sys.path.append("../sentiment-model-api-client")
from sentiment_model_api_client import Client
from sentiment_model_api_client.models import Input
from sentiment_model_api_client.api.default import predict_post

client = Client(base_url="http://localhost:8080", timeout=30)

predict_post.sync(client=client, 
                  json_body=Input(sentence=
                                  "I wonder how close a drone has to get to private property before someone "
                                  "can shoot it down, because that will definitely happen."))

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Experiment Tracking
#
# Experiment Tracking z.B. mit [MLflow](https://mlflow.org/)
#
# [Modell Training](train.pct.py)
#
# [MLFlow](http://localhost:5000)

# %% [markdown] slideshow={"slide_type": "slide"}
# # Monitoring
#
# [Model API](http://localhost:8080/docs)
#
# [Metrics Endpoint](http://localhost:8080/metrics)
#
# [Grafana](http://localhost:3000)
#
# [Call API](call_api.pct.py)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## 500 Aufrufe

# %% slideshow={"slide_type": "fragment"}
for idx, row in data_df.sample(500).iterrows():
    if not pd.isna(row["text"]) and row["text"] not in ["[deleted]", "[removed]"]:
        sentiment = predict_post.sync(client=client, json_body=Input(sentence=row["text"]))
        data_df.loc[idx, "sentiment"] = sentiment.label

# %% [markdown] slideshow={"slide_type": "fragment"}
# Ergebnisse

# %% slideshow={"slide_type": "-"}
with pd.option_context("display.max_colwidth", None):
    display(data_df[pd.notna(data_df["sentiment"])][["text", "sentiment"]].head())


# %% [markdown] slideshow={"slide_type": "slide"}
# # Monitoring
#
# ![dashboard showing distriubtions of models scores, outlier scores, labels and drifts over time](../images/dashboard.png)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Outlier Detection
# <img style="height:600px;" src="https://i.stack.imgur.com/3Ab7e.jpg" alt="Extrapolation" />
#
# [Outlier Detector](outlier_detector.pct.py)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Drift detection
#
# [Drift detection](drift_detector.pct.py)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Outlier Detection
# [Call API with outliers](call_api.pct.py)

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Automation

# %% slideshow={"slide_type": "-"} hideCode=true language="html"
# <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Machine learning pipelines <a href="https://t.co/5FpG3HrdW0">pic.twitter.com/5FpG3HrdW0</a></p>&mdash; AI Memes for Artificially Intelligent Teens (@ai_memes) <a href="https://twitter.com/ai_memes/status/1382374419666976771?ref_src=twsrc%5Etfw">April 14, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

# %% [markdown] slideshow={"slide_type": "slide"}
# ## What else?
# * Data Science development environment
# * Pull Requests
# * Test Automation
#     * Unit Tests
#     * Integration tests
# * Scaling (e.g. with Kubernetes)
# * Staging
# * CI/CD
# * security
# * ...
