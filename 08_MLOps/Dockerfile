#FROM docker-registry.default.svc:5000/daan-eval/python:3.8.10
FROM docker-registry.default.svc:5000/teambank-build/miniconda:4.7.12

EXPOSE 8080


USER root
RUN  mkdir /app && \
    rm /root/.condarc

WORKDIR /app

COPY . .
# COPY requirements.txt .
# COPY setup.py .
# COPY hamlops/. .

RUN conda env create -f environment_ops.yml && \
    conda init bash && \
    source ~/.bashrc && \
    cp ~/.bashrc . && \
    conda activate mlops && \
    /opt/conda/bin/conda clean -afy && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
#     find /opt/conda/ -follow -type f -name '*.js.map' -delete && \

# # RUN pip install -r requirements.txt --no-cache-dir && \
# #     pip install .

# # Modell aus Modell-Repository ziehen
# RUN source ~/.bashrc && conda activate mlops && \
    dvc remote modify --local minio access_key_id ${MINIO_ACCESS_KEY} && \
    dvc remote modify --local minio secret_access_key ${MINIO_SECRET_KEY} && \
    dvc config core.no_scm true && \
    dvc pull models/model.dvc

# Berechtigungen setzen
RUN chgrp -R 0 . && \
    chmod -R g=u . && \
    chmod -R g+rw . && \
    chmod a+x app/run.sh

USER 1001

WORKDIR /app

CMD ./app/run.sh