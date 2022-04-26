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
# ![MLOps](images/MLOps.jpg)

# %% [markdown] slideshow={"slide_type": "slide"}
# ![hidden technical debt paper](images/hidden_technical_debt_2015.jpg)

# %% [markdown] slideshow={"slide_type": "subslide"}
# * __Reproduzierbarkeit__: 
#     * Versionierung von Daten und Code
# * __Monitoring__:
#     * Überwachung des Verhaltens des Modells in Produktion

# %% [markdown] slideshow={"slide_type": "slide"}
# # Code
#
# * GitHub: https://github.com/datanizing/datascienceday/
# * Verzeichnis: `06_MLOps`

# %% [markdown] slideshow={"slide_type": "slide"}
# # Modell aus "Sprachmodelle und Sentiment-Analyse" (Oliver Zeigermann)
# ![Architektur Überblick](images/Architecture_Python.png)

# %% [markdown] slideshow={"slide_type": "slide"}
# # DVC mit Minio
# ![Architektur Überblick](images/Architecture_Minio.png)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## [DVC](https://dvc.org/)
#
# ![DVC_project_versions](https://dvc.org/static/39d86590fa8ead1cd1247c883a8cf2c0/fa73e/project-versions.webp)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## DVC Pipelines
#
# #### Daten laden
#
# ```
# python load_data.py
# ```

# %% slideshow={"slide_type": "fragment"}
# !dvc run -n load_data --no-exec --force -o data/raw/transport-short.csv -d load_data.py python load_data.py


# %% [markdown] slideshow={"slide_type": "subslide"}
# ## DVC Pipelines
#
# #### Model trainieren
#
# ```
# python train.py
# ```

# %%
# !dvc run -n train --no-exec --force -d data/raw/transport-short.csv -d train.py -o models/model/ python train.py

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## DVC Pipelines

# %% slideshow={"slide_type": "-"}
# !dvc dag --full | cat

# %% slideshow={"slide_type": "-"}
# !dvc dag --out | cat

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Pipelines
# In DVC lassen sich Pipelines definieren und damit lasse sich Trainings-Skripte und Daten miteinander verbinden.
# #### `dvc.yaml`

# %% [markdown]
# ```yaml
# stages:
#   train:
#     cmd: python train.py
#     deps:
#     - data/raw/transport-short.csv
#     outs:
#     - models/model/
#
# ```

# %% [markdown] slideshow={"slide_type": "subslide"}
# Reproduzieren der Schritte mit

# %%
# !dvc repro

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Datenstände
#
# Datenstände werden in `dvc.lock` über Hashes abgebildet.
# ```yaml
# stages:
#   load_data:
#     cmd: python load_data.py
#     deps:
#     - path: load_data.py
#       md5: ddeb3c7968c47788fb055752566e725d
#       size: 153
#     outs:
#     - path: data/raw/transport-short.csv
#       md5: 3057d4f316405b0a282328d2f9ee5748
#       size: 551260620
#   train:
#      ...
# ```

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## DVC Data
#
# Folgende Datenablagen werden unterstützt:
# * Amazon S3 (und kompatible, z.B. Minio)
# * Azure Blob Storage
# * Google Drive
# * Google Cloud Storage
# * Aliyon OSS
# * SSH
# * HDFS
# * WebHDFS
# * HTTP
# * WebDAV
# * local remote (z.B. Netzlaufwerke)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## DVC Remote
#
# Hier, [DVC Remote with Minio](http://localhost:9000/minio/dvcrepo/)
#
# * ACCESS KEY: `minio-access-key`
# * SECRET KEY: `minio-secret-key`

# %% slideshow={"slide_type": "fragment"}
# !dvc push

# %% slideshow={"slide_type": "fragment"}
# !dvc pull

# %% [markdown] slideshow={"slide_type": "slide"}
# # Docker Image mit API
# ![Architektur Überblick](images/Architecture_Docker.png)

# %% [markdown] slideshow={"slide_type": "subslide"}
# # Sentiment API
#
# Mittels [FastAPI](https://fastapi.tiangolo.com/) wird eine API für das Sentiment Model bereitgestellt.

# %% [markdown] slideshow={"slide_type": "subslide"}
# ### Datenmodell für Ein- und Ausgabe
#
# ##### `app.py`
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
# ##### `app.py`
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
# ##### `app.py`
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

# %%
# !openapi-python-client generate --url http://127.0.0.1:8080/openapi.json

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## API aufrufen

# %% slideshow={"slide_type": "fragment"}
import sys
sys.path.append("./sentiment-model-api-client")
from sentiment_model_api_client.client import Client
from sentiment_model_api_client.models import Input
from sentiment_model_api_client.api.default import predict_post

client = Client(base_url="http://localhost:8080", timeout=30)

predict_post.sync(client=client, 
                  json_body=Input(sentence=
                                  "I wonder how close a drone has to get to private property before someone "
                                  "can shoot it down, because that will definitely happen."))

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Docker Images bauen
#
# ##### `Dockerfile` (Auszug)
# ```Dockerfile
# FROM docker.io/bitnami/python:3.8.13
# ...
# RUN pip install -r requirements.txt --no-cache-dir 
#
# ...
# RUN dvc config core.no_scm true && \
#     dvc pull models/model/
#
# CMD uvicorn app:app --host=0.0.0.0 --port=8080
# ```

# %% slideshow={"slide_type": "subslide"}
# !docker build -t modelapi --network="host" .

# %% [markdown] slideshow={"slide_type": "slide"}
# # Orchestrierung mit Docker
# ![Architektur Überblick](images/Architecture_DockerCompose.png)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Docker-Compose Datei
# ```yaml
# version: "2"
# services:
#     modelapi:
#         image: modelapi
#         expose:
#         - 8080
#         ports:
#         - 8080:8080
#
#     minio:
#         image: docker.io/bitnami/minio:2021.6.17
#         ...
#         
#     prometheus:
#         image: docker.io/bitnami/prometheus:2
#         ...
#
#     grafana:
#         image: docker.io/bitnami/grafana:7
#         ...
# ```
#

# %% [markdown] slideshow={"slide_type": "-"}
# Starten mit
#
# ```
# docker-compose up
# ```

# %% [markdown] slideshow={"slide_type": "slide"}
# # Monitoring mit Prometheus/Grafana
# ![Architektur Überblick](images/Architecture_Grafana.png)

# %% [markdown] slideshow={"slide_type": "slide"}
# # Monitoring
#
# Modelausgaben über Header mitgeben, damit der Prometheus Client diese abfangen kann.
#
# #### `app.py`
# ```python
# # Endpunkt für Prediction
# @app.post('/predict', response_model=Sentiment, operation_id="predict_post")
# async def predict(response: Response, input: Input):
#     pred = sentiment_classifier(input.sentence)[0]
#     sentiment = Sentiment(**pred)
#
#     # Header Monitoring
#     response.headers["X-model-score"] = str(sentiment.score)`**
#     response.headers["X-model-sentiment"] = str(sentiment.label)`**
#
#     return sentiment
#

# %% [markdown] slideshow={"slide_type": "subslide"}
# Metriken definieren
#
# ```python
# from prometheus_client import Histogram, Counter
#
# def model_output(metric_namespace: str = "", metric_subsystem: str = ""):
#     SCORE = Histogram(
#         "model_score",
#         "Predicted score of model",
#         buckets=(0, .1, .2, .3, .4, .5, .6, .7, .8, .9),
#         namespace=metric_namespace,
#         subsystem=metric_subsystem,
#     )
#     ...
# ```

# %% [markdown] slideshow={"slide_type": "subslide"}
# ```python
#     ...
#     SENTIMENT = Counter(
#         "sentiment",
#         "Predicted sentiment",
#         namespace=metric_namespace,
#         subsystem=metric_subsystem,
#         labelnames=("sentiment",)        
#     )
#     ...
# ```

# %% [markdown] slideshow={"slide_type": "subslide"}
# Metriken aus Header auslesen
#
# ```python
#     ...
#     def instrumentation(info) -> None:
#         if info.modified_handler == "/predict":
#             model_score = info.response.headers.get("X-model-score")
#             model_sentiment = info.response.headers.get("X-model-sentiment")
#             if model_score:
#                 SCORE.observe(float(model_score))
#                 SENTIMENT.labels(model_sentiment).inc()
#
#     return instrumentation
# ```

# %% [markdown] slideshow={"slide_type": "subslide"}
# Metriken an `app` beobachten:
# ```python
# from prometheus_fastapi_instrumentator import Instrumentator
#
# instrumentator = Instrumentator()
# instrumentator.add(model_output(metric_namespace="mlops", metric_subsystem="model"))
#
# # Prometheus Instrumentator verknüpfen
# instrumentator.instrument(app).expose(app)
# ```

# %% [markdown] slideshow={"slide_type": "slide"}
# # Monitoring
#
# [Model API](http://localhost:8080/docs)
#
# [Metrics Endpoint](http://localhost:8080/metrics)
#
# [Grafana](http://localhost:3000)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## 500 Aufrufe
#
# #### Daten laden

# %% slideshow={"slide_type": "fragment"}
import pandas as pd
data_df = pd.read_csv("data/raw/transport-short.csv", header=None, nrows=1000, names=['id', 'kind', 'title', 'link_id', 'parent_id', 'ups', 'downs', 'score',
       'author', 'num_comments', 'created_utc', 'permalink', 'url', 'text',
       'level', 'top_parent'])
data_df.head(2)

# %% [markdown] slideshow={"slide_type": "subslide"}
# ### API mit 500 Samples aufrufen

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
# # [Dashboard](http://localhost:3000/d/PGUZYQznk/model-score?orgId=1&refresh=5s)
#
# ![dashboard showing distriubtions of models scores, outlier scores, labels and drifts over time](images/dashboard.png)
#
#

# %% [markdown] slideshow={"slide_type": "subslide"}
# ## Was kann man messen?
#
# * Score Verteilung
#    * Frühwarnindikator für Probleme
#    * Leichter zu messen als Modellgüte ("Was ist das korrekte Sentiment?")
# * Grundlegende Aufrufstatistiken
#    * Wird das Modell ggf. anders verwendet?
#    
# Komplexer, aber ggf. hilfreich:
# * Drift
#    * Seperates Modell notwendig ("Drift Detector")
#    * z.B. Themenschwerpunkte verschieben sich im Vergleich zum Trainingsdatensatz stark
# * Outlier Score
#    * Separate Modelle, die prüfen, ob Daten zu Trainingsdaten passen
#    * z.B. Anteil nicht-englischer Posts steigt
