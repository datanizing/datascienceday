#FROM docker-registry.default.svc:5000/daan-eval/python:3.8.10
FROM docker.io/bitnami/python:3.8.13

EXPOSE 8080


USER root

WORKDIR /app

COPY app.py .
COPY requirements.txt .
COPY models/model.dvc models/model.dvc
COPY .dvc/config .dvc/config
COPY .dvc/config.local .dvc/config.local

RUN pip install -r requirements.txt --no-cache-dir 

# # Modell aus Modell-Repository ziehen
# RUN source ~/.bashrc && conda activate mlops && \
RUN dvc config core.no_scm true && \
    dvc pull models/model.dvc

# Berechtigungen setzen
RUN chgrp -R 0 . && \
    chmod -R g=u . && \
    chmod -R g+rw . && \
    chmod a+x app.py

USER 1001

WORKDIR /app

CMD /app/app.py
