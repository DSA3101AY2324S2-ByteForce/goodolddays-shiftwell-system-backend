import pandas as pd
import schedule_generator

def predict_shift(config):

    if type(config) == list:
        df = pd.DataFrame(config)
    else:
        df = config
    
    y_pred = schedule_generator.schedule_employees(df)
    
    return y_pred
    