import numpy as np
import matplotlib.pyplot as plt

data = {
        "08/24": 17000,
        "09/24": 8230,
        "10/24": 5603,
        "11/24": 4000,
        "12/24": 5000,
        "01/25": 3049,
        "02/25": 3840,
        "03/25": 5776,
        "04/25": 8203,
        "05/25": 4563,
        "06/25": 5569,
        "07/25": 7033,
        "08/25": 7364,
        "09/25": 4503,
}
f'''
def unpack_data(data):
    lista = []
    for year, val1 in data.items():
        for month, val2 in val1.items():
            if type(val2) == int:
                lista.append(val2)
    return lista
'''


def promedio_movil(n, data):
    i = 0
    keys = list(data.keys())
    subdict = data.copy()

    # Loop through the array to consider
    # every window of size 3
    while i < len(data) - n :
        
        # Store elements from i to i+window_size
        # in list to get the current window
        window = list(data.values())[i : i + n]

        # Calculate the average of current window
        window_average = round(sum(window) / n, 2)
        
        # Store the average of current
        # window in moving average list
        
        subdict[keys[i+n]] = {"demanda" : data[keys[i+n]], "forecast" : window_average }

        # Shift window to right by one position
        i += 1
    return subdict

def naive(data):
    i = 1
    keys = list(data.keys())
    subdict = data.copy()

    # Loop through the array to consider
    # every window of size 3
    while i < len(data):


        # Store elements from i to i+window_size
        # in list to get the current window
        forecast = list(data.values())[i-1]

        subdict[keys[i]] = {"demanda" : data[keys[i]], "forecast" : forecast }

        # Shift window to right by one position
        i += 1
    return subdict

def acumulado(data):
    i = 0
    keys = list(data.keys())
    subdict = data.copy()

    # Loop through the array to consider
    # every window of size 3
    while i < len(data):
        
        # Store elements from i to i+window_size
        # in list to get the current window
        window = list(data.values())[0 : i+1]

        # Calculate the average of current window
        window_average = round(sum(window) / (i+1), 2)
        
        # Store the average of current
        # window in moving average list
        
        subdict[keys[i]] = {"demanda" : data[keys[i]], "forecast" : window_average }

        # Shift window to right by one position
        i += 1
    return subdict

def exponencial(i_forecast,alfa,data):
    i = 0
    keys = list(data.keys())
    subdict = data.copy()
    fcast = 0
    # Loop through the array to consider
    # every window of size 3
    while i < len(data) :
        
        if i == 0:
            subdict[keys[i]] = {"demanda" : data[keys[i]], "forecast" : i_forecast }
            fcast = i_forecast
            i += 1
        else:
            # Store elements from i to i+window_size
            # in list to get the current window
            window = list(data.values())[i-1]

            # Calculate the average of current window
            window_average = fcast*(1 - alfa) + window * alfa
            
            # Store the average of current
            # window in moving average list
            
            subdict[keys[i]] = {"demanda" : data[keys[i]], "forecast" : window_average }

            # Shift window to right by one position
            fcast = window_average
            i += 1
    return subdict


def weighted_moving_average(w: list, data):
    i = 0
    keys = list(data.keys())
    subdict = data.copy()

    # Loop through the array to consider
    # every window of size 3
    while i < len(data) - len(w) :
        
        # Store elements from i to i+window_size
        # in list to get the current window
        window = list(data.values())[i : i + len(w)]

        # Calculate the average of current window
        lista = []
        for n in range(0, len(window)):
            lista.append(window[n]*w[n])
        window_average = sum(lista)
        # Store the average of current
        # window in moving average list
        
        subdict[keys[i + len(w)]] = {"demanda" : data[keys[i + len(w)]], "forecast" : window_average }

        # Shift window to right by one position
        i += 1
    return subdict


#lista = unpack_data(data)
#di = weighted_moving_average([0.4, 0.6], data)
di = promedio_movil(2,data)
print(di)
