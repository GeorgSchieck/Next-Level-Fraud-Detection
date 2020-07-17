# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:57:29 2020

@author: Bjarne
"""
from joblib import load

class ModelRuntime():
    
    def __init__(self,model="./ModelStorage/saved_model.pkl", threshold = 0.35):
        """
        Diese Klässe lädt das Modell und kann
        zur Laufzeit verwendet werden, um Vorhersagen
        zu treffen.

        Parameters
        ----------
        model : str
            Pfad zum Pickle-File des Modells.

        Returns
        -------
        None.

        """
        self.model = load("./ModelStorage/saved_model.pkl")
        self.threshold = threshold
        
    def predict(self, data):
        """
        Verwendes des Modells für ein Sample

        Parameters
        ----------
        data : list
            Datensatz, den es zu interpretieren gilt.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.model.predict_proba([data])[0][1] >= self.threshold
