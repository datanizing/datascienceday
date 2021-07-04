from prometheus_client import Histogram, Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info

NAMESPACE = "mlops"
SUBSYSTEM = "model"

instrumentator = Instrumentator()
instrumentator.add(metrics.request_size(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM))
instrumentator.add(metrics.response_size(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM))
instrumentator.add(metrics.latency(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM))
instrumentator.add(metrics.requests(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM))

def model_output(metric_namespace: str = "", metric_subsystem: str = ""):
    SCORE = Histogram(
        "model_score",
        "Predicted score of model",
        buckets=(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1, 1.1),
        namespace=metric_namespace,
        subsystem=metric_subsystem,
    )
    SENTIMENT = Counter(
        "sentiment",
        "Predicted sentiment",
        namespace=metric_namespace,
        subsystem=metric_subsystem,
        labelnames=("sentiment",)        
    )

    def instrumentation(info: Info) -> None:
        if info.modified_handler == "/predict":
            model_score = info.response.headers.get("X-model-score")
            model_sentiment = info.response.headers.get("X-model-sentiment")
            if model_score:
                SCORE.observe(float(model_score))
                SENTIMENT.labels(model_sentiment).inc()

    return instrumentation

instrumentator.add(model_output(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM))
