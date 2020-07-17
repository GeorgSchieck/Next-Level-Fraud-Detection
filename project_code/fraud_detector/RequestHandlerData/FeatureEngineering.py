# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 18:29:55 2020

@author: Bjarne
"""
import ORM_Datamodel as ORM
# Beginnend werden die Daten über vergangene Frauds geladen.
# So wird vermieden, dass dies bei jeder Prädiktion erneut geschehen muss
# zur Datenbank verbinden
session = ORM.CreateSession()

# Anzahl aller Transaktionen bestimmen
# Dies wird zu beginn ausgeführt, da der Wert in Millionenhöhe ist
# und leichte veränderungen die daraus erstellten Werte nur gering verändern.
# So werden unnötigte Berechnungen verhindert.
all_tx_nb = session.query(ORM.Transaction).count()


class FeatureEngineering:
    
    def __init__(self,transformed_data):
        # Transformierter Datensatz der aktuellen Transaktion
        self.transformed_data = transformed_data
        
        self.features = dict()
        
    def Transform(self):
        # Bereits bekannte Features übertragen
        self.features["amount"] = self.transformed_data["amount"]
        self.features["oldbalanceOrg"]= self.transformed_data["oldbalanceOrg"]
        self.features["newbalanceOrig"]= self.transformed_data["newbalanceOrig"]
        
        # Prozentuale veränderung des Guthaben:
        # Betrüger versuchen üblicherweise den größtmöglichen Anteil aus einem
        # Account zu transferieren
        
        # Hier wurde Laplace Smoothing verwendet, um zu verhindern,
        # dass fehlerhafte Kontostände inf-Werte auftreten, da der Datenstamm teilweise Werte nicht angegeben hat.
        self.features["PctChangeOrg"] = (self.transformed_data["amount"]+1) / (self.transformed_data["oldbalanceOrg"]+1)
        
        # Tageszeit aus step ableiten:
        self.features["HourOfTheDay"] = self.transformed_data["step"] % 24
        
        # Relativer Anteil aller Transaktionen zum Zahlungsempfänger:
        self.features["RelativePctTxToDest"] = session.query(ORM.Transaction)\
                                    .filter(ORM.Transaction.nameDest == self.transformed_data["nameDest"]).count()\
                                        /all_tx_nb
            
      	# Hier sind noch weitere Features erstellt worden, 
        # welche aber ENTFERNT worden sind      

        # Beispielsweise: Transaktionen zwischen den Beteiligten
        #                   Transaktionen des Senders etc.
        # Anzahl der Transaktion zum Empfängers     
 
        # Dummyvariablen aus der Variable "Type" erstellen
        self.features["CASH_IN"] = 0
        self.features["CASH_OUT"] = 0
        self.features["DEBIT"] = 0
        self.features["PAYMENT"] = 0
        self.features["TRANSFER"] = 0
        self.features[self.transformed_data["type"]] = 1
        
        return self.features
