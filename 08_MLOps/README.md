# MLOps

## OpenShift Komponenten laden
```
oc process -f deployment/minio.yml | oc apply -f -
oc process -f deployment/prometheus.yml | oc apply -f -
oc process -f deployment/modelapi.yml | oc apply -f -
```

Ggf Pods forwarden:
```
oc port-forward svc/grafana 8888:3000
oc port-forward svc/prometheus 9090:9090
```


## DVC einrichten

```
dvc remote add -d minio s3://dvcrepo
dvc remote modify minio endpointurl http://ha-mlops-minio-myproject.127.0.0.1.nip.io/ 
dvc remote modify --local minio access_key_id 'ssge333434'
dvc remote modify --local minio secret_access_key 'sdsge343sfSFFDFDF'
```


## API lokal testen

Mit folgendem Befehl kann die API lokal getestet werden.

```
python -m app.app
```

OpenAPI Client aus Spezifikation generieren:
```
openapi-python-client generate --url http://127.0.0.1:8080/openapi.json
```


Mountpoint /usr/share/grafana/conf/provisioning/dashboards/default-provider.yml

```yaml
apiVersion: 1
providers:
  - name: "default"
    orgId: 1
    folder: ""
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /usr/share/grafana/conf/provisioning/dashboards
```

References:
* [fastAPI](https://fastapi.tiangolo.com/)
* [dvc](https://dvc.org/)
* [openapi-python-client](https://github.com/openapi-generators/openapi-python-client)
* [OpenShift](https://www.openshift.com/)
* [minishift](https://docs.okd.io/3.11/minishift/getting-started/index.html)
* [Grafana](https://grafana.com/)
* [Prometheus](https://prometheus.io/)
* [prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)