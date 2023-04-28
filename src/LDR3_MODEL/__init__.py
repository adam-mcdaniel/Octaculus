import numpy as np
import pandas as pd
import pickle
import os

class LDR3_MODEL(object):
    def __init__(self):
        self.pkl_filename = './3LDR_RF.sav'
        
        try:
            self.RFmodel = self.load_model_from_file()

        except Exception as e:
            print(e)
            raise AttributeError("Could not find something; check installation")
        finally:
            pass

    def load_model_from_file(self):
        # Load from file
        try:
            with open(self.pkl_filename, 'rb') as file:
                pickle_model = pickle.load(file)
            return pickle_model
        finally:
            print(os.getcwd())



    def model_predict(self, data):
        ypred = self.RFmodel.predict(data)
        rtn = int(ypred)        
        return rtn