#Importing libraries
import pandas as pd
import numpy as np
import scipy as sci
import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline

import os, sys
print(os.getcwd()) # current working directory

output_file = pd.read_csv('OutputCities.csv',sep=';',header=0)

distance = pd.read_csv("TR81_KGM_csv.csv",sep=';')

distance.index = distance['IL ADI']

del distance['IL NO']
del distance['IL ADI']
del distance['IL ADI.1']
del distance['IL NO.1']


output_file['starting'] = output_file['A'].map(lambda x: str(x).split(',')[1])
output_file['going'] = output_file['starting'].map(lambda x: int(str(x)[:-1]))

cities_list = list(distance.columns.values)
cities_series = pd.Series(cities_list)
cities_number = list(range(82))
del cities_number[0]


output_file['leaving'] = output_file['A'].map(lambda x: int(str(x).split(',')[0][2:]))

output_file.index = output_file.index + 1

route = []

starting_destination=51

route.append(starting_destination)
for i in range(80):
    route.append(output_file['going'][starting_destination])
    starting_destination = output_file['going'][starting_destination] 

city_centers = pd.read_csv('city_centers.csv',sep=';',encoding='cp857')

city_centers = city_centers[['A','B','C']]

city_centers['A'] = cities_series

labels = cities_list


data = city_centers[['B','C']].values

city_centers['A'] = pd.Series(cities_number)
city_centers.index = city_centers.index + 1

city_centers['B'] = city_centers['B'].map(lambda x: round(x,3))
city_centers['C'] = city_centers['C'].map(lambda x: round(x,3))

latitude=[]
longitude=[]
for i in route:
    latitude.append(city_centers['B'][i])
    longitude.append(city_centers['C'][i])

#Adding starting point to the end for convenience
latitude.append(latitude[0])
longitude.append(longitude[0])
dict1={'lat':latitude,'lon':longitude}
df1 = pd.DataFrame(dict1)

plt.figure(figsize=(23,10))
plt.plot(list(df1['lon']),list(df1['lat']),'o-',color='red',label=labels)
plt.ylabel("Latitude",size=20)
plt.xlabel("Longitude",size=20)
plt.title('Starting from Nigde ending at Nevsehir')
for label, x, y in zip(labels, data[:, 1], data[:, 0]):
    plt.annotate(
        label,
        xy=(x, y), xytext=(-20, 20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
plt.show()


