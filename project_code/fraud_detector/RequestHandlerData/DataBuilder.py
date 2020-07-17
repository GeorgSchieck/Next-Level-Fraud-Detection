# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 12:39:20 2020

@author: Bjarne
"""
import sys
sys.path.append("..")
from sqlalchemy import create_engine
import pandas as pd
import ORM_Datamodel as ORM

# Zur Datenbank verbinden
session = ORM.CreateSession()


class DataBuilder:
    
    def __init__(self, amount, type_name, nameOrig, nameDest, step):
        # Variablen initialisieren
        self.amount = amount
        self.type = type_name
        self.nameOrig = nameOrig
        self.nameDest = nameDest
        self.step = step
        
        # Datenspeicher initializieren
        self.df_data = None
        self.transformed_data = dict()
        
    def GetRelevantData(self):
        # Importieren der benötigten Daten für das Feature Engineering mittels SQLAlchemy
        self.oldbalanceOrg = round(float(session.query(ORM.Transaction)\
                       .filter(ORM.Transaction.nameOrig == self.nameOrig)\
                           .order_by(ORM.Transaction.tx_id.desc())\
                               .first().newbalanceOrig),2)

        self.oldbalanceDest = round(float(session.query(ORM.Transaction)\
                       .filter(ORM.Transaction.nameDest == self.nameDest)\
                           .order_by(ORM.Transaction.tx_id.desc())\
                               .first().newbalanceDest),2)
        

    def DataTransformation(self):
        # Ableiten der benötigten Daten aus den Benutzereingaben
        # Hier wird aus den eben bezogenen Daten nun weiteres, wie die Kontostand, abgeleitet
        self.transformed_data["step"] = self.step
        self.transformed_data["type"] = self.type
        self.transformed_data["amount"] = self.amount
        self.transformed_data["nameOrig"] = self.nameOrig
        self.transformed_data["oldbalanceOrg"] = self.oldbalanceOrg
        self.transformed_data["newbalanceOrig"] = self.oldbalanceOrg - self.amount
        self.transformed_data["nameDest"]  = self.nameDest
        self.transformed_data["oldbalanceDest"] = self.oldbalanceDest
        self.transformed_data["newbalanceDest"] = self.oldbalanceDest + self.amount
       
        return self.transformed_data