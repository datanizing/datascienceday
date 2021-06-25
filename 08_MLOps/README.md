# MLOps

Sentiment Datensatz IMDB bezogen hier:

http://ai.stanford.edu/~amaas/data/sentiment/

Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. (2011). Learning Word Vectors for Sentiment Analysis. The 49th Annual Meeting of the Association for Computational Linguistics (ACL 2011).

```
wget IMDB Dataset


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