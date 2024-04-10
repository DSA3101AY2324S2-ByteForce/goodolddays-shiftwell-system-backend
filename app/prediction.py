import pandas as pd
import schedule_generator
import schedule_generator_economic

def predict_shift_economic(config):

    if type(config) == list:
        df = pd.DataFrame(config)
    else:
        df = config
    
    y_pred = schedule_generator_economic.schedule_employees(df)
    
    return y_pred
    