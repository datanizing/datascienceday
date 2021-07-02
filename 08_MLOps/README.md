# MLOps

Sentiment Datensatz IMDB bezogen hier:

http://ai.stanford.edu/~amaas/data/sentiment/

Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. (2011). Learning Word Vectors for Sentiment Analysis. The 49th Annual Meeting of the Association for Computational Linguistics (ACL 2011).

```
wget IMDB Dataset

https://127.0.0.1:8443/console/catalog

Containt Suche RedHat:
https://catalog.redhat.com/software/containers/search

Helm:
wget https://get.helm.sh/helm-v3.6.1-linux-amd64.tar.gz

helm repo add bitnami https://charts.bitnami.com/bitnami

helm template bitnami/minio --set ingress.enabled=true > deployment/minio.yml

oc process -f deployment/minio.yml | oc apply -f -

http://ha-mlops-minio-myproject.127.0.0.1.nip.io/minio/login

wget https://dl.min.io/client/mc/release/linux-amd64/m
chmod +x mc
sudo mv mc /usr/bin/.

mc alias set minio http://ha-mlops-minio-myproject.127.0.0.1.nip.io/ ssge333434 sdsge343sfSFFDFDF --api S3v4

dvc remote add -d minio s3://dvcrepo
dvc remote modify minio endpointurl http://ha-mlops-minio-myproject.127.0.0.1.nip.io/ 
dvc remote modify --local minio access_key_id 'ssge333434'
dvc remote modify --local minio secret_access_key 'sdsge343sfSFFDFDF'

oc process -f deployment/prometheus.yml | oc apply -f -

oc port-forward svc/grafana 8888:3000
oc port-forward svc/prometheus 9090:9090


dvc run -n train -d data/interim/model_dev_data.pkl -o models/model.pkl -M score.json python -m hamlops.train

mlflow ui --backend-store-uri file://mlruns

oc process -f deployment/modelapi.yml | oc apply -f -

oc start-build ha-mlops-modelapi-build --from-dir=. --follow

oc import-image python-38:1-61 --from=registry.redhat.io/rhel8/python-38:1-61 -n myproject 

Explainer Response HTML: https://fastapi.tiangolo.com/advanced/custom-response/#html-response

Extrapolation: https://stats.stackexchange.com/questions/219579/what-is-wrong-with-extrapolation

oc project daan-build

oc apply -f deployment\import_images.yml

python app/app.py

