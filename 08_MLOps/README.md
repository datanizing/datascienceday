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

Daten per dvc holen:
```
dvc pull
```

## Starten der API:

```
python app.py
```

## Setup aus Prometheus, Grafana und Model API starten

Voraussetzung: 
* lokale [Docker](https://docs.docker.com/get-docker/) Installation

```
docker-compose
```

## Referenzen:
* [fastAPI](https://fastapi.tiangolo.com/)
* [pydantic]()
* [dvc](https://dvc.org/)
* [openapi-python-client](https://github.com/openapi-generators/openapi-python-client)
* [prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
* [Docker](https://docs.docker.com/get-docker/)
* [OpenShift](https://www.openshift.com/)
* [minishift](https://docs.okd.io/3.11/minishift/getting-started/index.html)
* [Grafana](https://grafana.com/)
* [Prometheus](https://prometheus.io/)
