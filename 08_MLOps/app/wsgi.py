"""
Dieses Modul stellt ein Web Server Gateway Interface bereit, dass 
eine Swagger API bereitstellt, um das Modell aufzurufen.
Ausführung im Entwicklungsmodus:
```
python wsgi.py
```
"""

from flask import Flask, request, jsonify
from flask_restplusx import Resource, Api, fields
import joblib
import pandas as pd

# Erzeugen der Flask WSGI Anwendung
application = Flask(__name__) 

# Swagger API erzeugen
api = Api(application, validate=True)

# Modell laden
clf = joblib.load("models/model.pkl")

# Im folgenden Code werden die Ein- und Ausgabefelder exakt 
# für die Swagger API definiert. Dieser Code muss jeweils auf 
# das Problem angepasst werden.

# Datenmodell der Eingabe
request_fields = api.model("Input", {
    "sepal length (cm)": fields.Float(required=True, description="sepal length (cm)", example=2.4),
    "sepal width (cm)": fields.Float(required=True, description="sepal width (cm)", example=2.4),
    "petal length (cm)": fields.Float(required=True, description="petal length (cm)", example=2.4),
    "petal width (cm)": fields.Float(required=True, description="petal width (cm)", example=2.4),
})

# Datenmodell der Ausgabe
response_fields = api.model("Response", {
    "pred": fields.String(description="Prediction", example="versicolor")
})

# Dieser Code definiert die Schnittstelle zum Modell
# und wird über die Route /v1 aufgerufen.
@api.route('/v1', methods=["post"])
class Predict(Resource):
    @api.expect(request_fields)
    @api.response(200, "Success", response_fields)
    def post(self):
        # Hier ggf. das JSON Eingabe-Objekt in den vom Modell
        # erwarteten Datentyp ändern.
        content = request.get_json()
        df = pd.DataFrame.from_dict([content])
        response_obj = {"pred": clf.predict(df)[0]}
        return jsonify(response_obj)

if __name__ == '__main__':

    application.run(debug=True)                #  Start a development server