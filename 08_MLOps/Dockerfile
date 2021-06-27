FROM bitnami/python:3.8.10-debian-10-r47

EXPOSE 8080


USER root

WORKDIR /app

COPY . .
# COPY requirements.txt .
# COPY setup.py .
# COPY hamlops/. .


RUN pip install -r requirements.txt --no-cache-dir && \
    pip install .

# Modell aus Modell-Repository ziehen
RUN dvc remote modify --local minio access_key_id '${MINIO_ACCESS_KEY}' && \
    dvc remote modify --local minio secret_access_key '${MINIO_SECRET_KEY}' && \
    dvc config core.no_scm true && \
    dvc pull models/model.pkl

# Berechtigungen setzen
RUN chgrp -R 0 . && \
    chmod -R g=u . && \
    chmod -R g+rw . && \
    chmod a+x app/run.sh

USER 1001

WORKDIR /app/app

CMD ./run.sh