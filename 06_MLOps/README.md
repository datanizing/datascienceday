# MLOps

## Voraussetzungen
* Conda Installation (z.B. [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
* Base Umgebung mit Jupyter, [nb_conda](https://anaconda.org/conda-forge/nb_conda) und [jupytext](https://jupytext.readthedocs.io/en/latest/install.html)
## Einrichtung

Nach dem Checkout zunächst die conda Umgebung erstellen und aktivieren:
```
git clone https://github.com/datanizing/datascienceday.git
cd datascienceday
cd 08_MLOps
conda env create -f environment.yml
conda activate mlops
```

Daten per dvc erzeugen:
```
dvc repro
```

## Starten der API:

```
python app.py
```

## API erzeugen

Während die Model API läuft, folgendes ausführen:
```
openapi-python-client generate --url http://127.0.0.1:8080/openapi.json
```


## Setup aus Prometheus, Grafana und Model API starten

Voraussetzung: 
* lokale [Docker](https://docs.docker.com/get-docker/) Installation

Da zunächst kein `modelapi` Image vorhanden ist, wird beim ersten Starten `docker-compose` einen Fehler werfen. 
Das kann vermieden werden, indem der entsprechende Abschnitt (`modelapi:`) auskommentiert wird und erst nach dem Bauen
des Image wieder einkommentiert wird.

```
docker-compose up
```

Dann das Image bauen:
```
docker build -t modelapi --network="host" .
```
Anschließend alle Services neu starten:
```
docker-compose down
docker-compose up
```

Das Dashboard kann dann unter http://localhost:3000/ nach dem Login  (User: admin, Passwort: 12345) im Bereich Dashboards ("Model Score") aufgerufen werden.

![Dashboard](images/dashboard.png)
Inspired by [Jeremy Jordan
A simple solution for monitoring ML systems.
](https://www.jeremyjordan.me/ml-monitoring/)

## Referenzen:
* [fastAPI](https://fastapi.tiangolo.com/)
* [pydantic](https://pydantic-docs.helpmanual.io/)
* [dvc](https://dvc.org/)
* [openapi-python-client](https://github.com/openapi-generators/openapi-python-client)
* [prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
* [Docker](https://docs.docker.com/get-docker/)
* [OpenShift](https://www.openshift.com/)
* [minishift](https://docs.okd.io/3.11/minishift/getting-started/index.html)
* [Grafana](https://grafana.com/)
* [Prometheus](https://prometheus.io/)




# Troubleshooting

## error checking context
Fehlermeldung:
```
error checking context: 'no permission to read from '/.../datascienceday/06_MLOps/docker-compose/minio/data/.access_key''.
```

Die Rechte müssen ausgeweitet werden, damit auch der User wieder auf die vom Docker Host angelegten Verzeichnisse zugreifen kann.
```
sudo chmod -R a+rw docker-compose/minio
```