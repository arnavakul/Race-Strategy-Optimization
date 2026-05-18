import numpy as np

def mae(actual, predicted):
    
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    return np.mean(abs(actual-predicted))
    
def rmse(actual, predicted):
    
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    return np.sqrt(np.mean(actual-predicted)**2)

def mape(actual, predicted):
    
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    return np.mean(
        np.abs((actual-predicted) / actual)
    ) * 100
    

def r2(actual, predicted):
    
    actual= np.array(actual)
    predicted = np.array(predicted)
    
    ss_res = np.sum(
        (actual - predicted) ** 2
    )
    
    ss_tot = np.sum(
        (actual - np.mean(actual)) ** 2 
    )
    
    return 1 - (ss_res/ss_tot)