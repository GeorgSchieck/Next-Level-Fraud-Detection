import sys
import flask
from flask import request, make_response
from flask_cors import CORS
from datetime import datetime

sys.path.append("./RequestHandlerData/")
sys.path.append("./RequestHandlerModel/")

# Importieren dauert bewusst ein wenig länger,
# Hier werden sich wiederholende DB-Abfragen durchgeführt
# Dies ermöglicht im Aktiven Einsatz höhere Performanz
from RequestHandlerData import DataBuilder
from RequestHandlerData import FeatureEngineering
from RequestHandlerData import ORM_Datamodel as ORM
from RequestHandlerModel import Predict
from RequestHandlerModel import Retrain

app = flask.Flask(__name__)
CORS(app)

session = ORM.CreateSession()

step = datetime.today().hour + 744


@app.route('/post/tx', methods=['POST'])
def post_tx():
    data = request.get_json()
    if data:
        amount = data["amount"]
        type_name = data["type"]
        nameOrig = str(data["nameOrig"])
        nameDest = str(data["nameDest"])

        isFraud = TX(amount, type_name, nameOrig, nameDest, step)
        result = make_response(str(isFraud))
        result.headers["Access-Control-Allow-Origin"] = '*'
        return result
    else:
        result = make_response("Fail")
        result.headers["Access-Control-Allow-Origin"] = '*'
        return result


@app.route('/post/model', methods=['POST'])
def post_model():
    dt_string_start = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    NewModell()
    dt_string_end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    result = make_response(f"Creation of New Model started at: {dt_string_start}, finished at: {dt_string_end}")
    result.headers["Access-Control-Allow-Origin"] = '*'
    return result


# Szenario: Kundentransaktion
def TX(amount, type_name, nameOrig, nameDest, step):
    # Bei Step bin ich unsicher, wie wird damit umgehen
    # Würde aber vorschlagen eine Differenz in Stunden zu
    # Tag X zu nehmen
    builder = DataBuilder.DataBuilder(amount, type_name, \
                                      nameOrig, nameDest, step)
    builder.GetRelevantData()
    data = builder.DataTransformation()
    oldbalanceOrg = data["oldbalanceOrg"]
    newbalanceOrig = data["newbalanceOrig"]
    oldbalanceDest = data["oldbalanceDest"]
    newbalanceDest = data["newbalanceDest"]

    session.add(
        ORM.Transaction(amount=amount, type=type_name, nameOrig=nameOrig,
                        nameDest=nameDest, step=step, oldbalanceOrg=oldbalanceOrg, newbalanceOrig=newbalanceOrig,
                        oldbalanceDest=oldbalanceDest, newbalanceDest=newbalanceDest))
    session.commit()

    Features = FeatureEngineering.FeatureEngineering(data)
    data = Features.Transform()

    return Predict.ModelRuntime().predict(list(data.values()))


# Szenario: Modellupdate
def NewModell():
    Retrain.Training(False, \
                     Retrain.MLAlgo.Model, \
                     Retrain.MLAlgo.params).Process()



# Beispielhafte Transaktionsanfrage

#amount = 2039491049.20
#type_name = "TRANSFER"
#nameOrig = "C336307904"
#nameDest = "C1155915285"
#step = 801
# TX(amount, type_name, nameOrig, nameDest, step)


# Neues Modell erstellen
# NewModell()
app.run(host='0.0.0.0', port=1213)

