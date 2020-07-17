# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 21:47:06 2020

@author: Bjarne
"""
import pandas as pd
import numpy as np
import sys
sys.path.append("..")
from RequestHandlerData import ORM_Datamodel as ORM
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import  train_test_split
from sklearn.metrics import  classification_report
from sklearn.metrics import f1_score
from datetime import datetime
from joblib import dump
import MLAlgorithm as MLAlgo
 
class DataHandler:
    
    def __init__(self):
        """
        Es wird der Datensatz aus der Datenbank bezogen und
        im folgenden an die Klasse "Training" übergeben.

        Returns
        -------
        None.

        """
        # Daten aus der Datenbank abfragen
        self.X = pd.read_sql_table('Transaction_preprocessed', ORM.connection_string).set_index("tx_id").sort_index()
        self.y = pd.read_sql_table('Transaction_Rating', ORM.connection_string).set_index("tx_id").sort_index()
        
    def FilterData(self):
        """
        Der Datensatz wird gefiltert, da die IsFraud-Variable direkt nach
        der Transaktion zwar in der Tabelle "Transaction_Rating"
        geschrieben wird, aber die Spalte "isFraud" zum Transaktionszeitpunkt
        nicht bekannt ist. Jene Einträge, dessen Ausprägung noch nicht bekannt ist,
        wird entfernt.

        Returns
        -------
        None

        """
        self.X = self.X[self.y.isFraud != np.nan]
        self.y = self.y[self.y.isFraud != np.nan]["isFraud"]
    
    def SplitData(self):
        """
        Test-Train-Split durchführen. 
        Die Testdaten werden als validierung verwendet, nach der Durchführung
        der GridSearch. Es wird also indirekt ein 3-Fold-Split eingeleitet.
        
        Der Parameter shuffle=False der Funktion train_test_split, wird
        verwendet, um keine Data Leakage zu erhalten durch beispielswiese,
        Betrüger, die mehrere illegale Transaktionen ausführen.
        
        Returns
        -------
        None.

        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(\
                                            self.X, self.y, train_size=0.8, random_state=42,\
                                                shuffle=False)
    
    def Process(self):
        self.FilterData()
        self.SplitData()
        
        
class Training:
    
    def __init__(self, isTuned, Model, params, DataHandler=DataHandler, threshold=0.5):
        """
        Diese Klasse koordiniert das Training. Es wird entschieden, ob das Modell
        in der finalen Form vorliegt oder Parametertuning durchgeführt werden muss,
        dabei ist die Klasse mit verschiedenen Modellen und Parameterpaaren,
        verwendbar.

        Parameters
        ----------
        isTuned : bool
            Rückschluss darüber, ob das Parametertuning notwendig ist.
            
        Model : class
            Enthält ML-Algorithmus, welcher verwendet werden soll.
            
        params : dict
            Enthält entweder Parameterpaare, sofern isTuned == False ist,
            oder aber die zu verwendenden Parameter für das finale Modell
            
        DataHandler : class
            Übergabe der DataHandler-Classe, um die Daten verarbeiten zu können.
        
        threshold : float
            Beschreibt den Grenzwert, ab welcher Wahrscheinlichkeit, eine 
            Transaktion als Fraud geflaggt wird.
            
        Returns
        -------
        None.
        """
        self.isTuned = isTuned
        self.Model = Model
        self.params = params
        self.DataHandler = DataHandler()
        self.threshold = threshold
        # Datenaufbereitung und split durchführen
        self.DataHandler.Process()
            
    def Process(self):
        """
        Unterscheidung danach, ob das Modell bereits optimiert worden ist.
        Ist dies nicht der Fall, wird die GridSearch eingeleitet, welche
        dann mit dem finalen Modell 

        Returns
        -------
        None.

        """
        if self.isTuned == True:
            # Train Model
            model = self.Model(n_jobs=-1, **self.params)
            model.fit(self.DataHandler.X, self.DataHandler.y)
            
            # Save model to storage    
            dump(model, './ModelStorage/saved_model.pkl')
        else:
            # Wenn  die Parameter nicht optimiert worden sind, leite GridSearch ein
            self.test = GridSearchTuning(self)
            self.test.Process()
            
class GridSearchTuning:
    
    def __init__(self, TrainingInstance,\
                 threshold_metric = 0.98):
        """
        

        Parameters
        ----------
        TrainingInstance : class
            Beschreibt eine Instanz der Training-Klasse. So werden
            Parametr ausgetauscht und können von dieser Klasse aus verändert werden.
            Wird benötigt, um das Optimale Parameterpaar zu inserten.
            
        threshold_metric : Schwellwert der Zielmetrik, optional
            Dieser Wert beschreibt den Schwellwert, ab dem ein Modell als "gut genug",
            gilt. The default is 0.98.

        Returns
        -------
        None.

        """
        # Übertragen der Parameter aus der Trainingsinstanz
        self.TrainingInstance = TrainingInstance
        self.X_train = TrainingInstance.DataHandler.X_train
        self.X_test = TrainingInstance.DataHandler.X_test
        self.y_train = TrainingInstance.DataHandler.y_train
        self.y_test = TrainingInstance.DataHandler.y_test
        self.threshold = TrainingInstance.threshold
        self.Model = TrainingInstance.Model
        self.params = TrainingInstance.params
        
        # Wir evaluieren das Modell auf der durchschnittlichen Präzision,
        # um eine verfälschung durch Imbalanced Data zu verhindern.
        # Es ist bewusst der durchschnittliche Wert verwendet worden,
        # da auch False Negatives einen Imageschaden verursachen.
        self.GridSearch = GridSearchCV(self.Model(), self.params, cv=2, n_jobs=-1, scoring='f1')
  
        # Schwellwerte übertragen
        self.threshold_metric = threshold_metric
        
    def ModelSelection(self):
        """
        Durchführen des eigentlichen Parametertunings und
        Rückgabe des besten auf Basis der Traininsdatensatzes.

        Returns
        -------
        None.

        """
        self.GridSearch.fit(self.X_train, self.y_train)
        
    def ModelValidation(self):
        """
        Validierung des Modells und zulassen des Modells, sofern
        die Schwellwerte nicht verletzt worden sind.        
        
        Returns
        -------
        None.

        """
        self.validation_model = self.Model(n_jobs=-1, **self.GridSearch.best_params_)
        self.validation_model.fit(self.X_train, self.y_train)
        
        y_pred = self.validation_model.predict_proba(self.X_test)
        # Wahrscheinlichkeiten in binäre Aussage umwandeln
        y_pred_binary = [y[1] >= self.threshold for y in y_pred]
        
        # F1-Score ermitteln erstellen 
        metric = f1_score(self.y_test, y_pred_binary)
        
        # Modellreport erstellen, um Modellgüte nachvollziehbar zu dokumentieren
        report = pd.DataFrame(classification_report(self.y_test, y_pred_binary, output_dict=True))
        report.to_csv(f"./ModelReport/report{str(datetime.now()).replace(':','-')}.csv")

        if self.threshold_metric <= metric:
            # Anpassen der Parameter der Trainingsinstanz
            self.TrainingInstance.isTuned = True
            self.TrainingInstance.params = self.GridSearch.best_params_
            # Trainieren und speichern des finalen Models
            self.TrainingInstance.Process()
        else:
            raise Exception("""Modelgüte nicht ausreichend. Prozess terminiert.
                            Das bestehende Modell wird beibehalten""")

    def Process(self):
        """
        Automatisiertes durchführen der benötigten Schritte
        """
        self.ModelSelection()
        self.ModelValidation()

