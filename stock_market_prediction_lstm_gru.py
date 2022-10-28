# -*- coding: utf-8 -*-
"""Copy of Stock_Market_Prediction_LSTM_GRU.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KHn5fu1r2NZmJe2Id5O2e-ktndw_VXBC
"""



"""STOCK MARKET PREDICTION: LSTM VS GRU"""

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics
from sklearn.metrics import mean_squared_error
from keras import optimizers
from keras.models import load_model
from keras.models import Sequential
from keras.layers import LSTM, GRU, Dense, Dropout
import tensorflow as tf

df = pd.read_csv('AMZN.csv')

df.head()

df.dtypes

df1=df.reset_index()['Date,Close']

df1

plt.plot(df1)

scaler = MinMaxScaler(feature_range=(0,1))
df1 = scaler.fit_transform(np.array(df1).reshape(-1,1))

import seaborn as sns 

plt.figure(figsize=(20, 6))
sns.barplot(x='prices',y='prices',hue='color',data=df1);
plt.xticks(rotation=90)

df1

##splitting dataset into train and test split
training_size=int(len(df1)*0.65)
test_size=len(df1)-training_size
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]

training_size,test_size

# convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

# reshape into X=t,t+1,t+2,t+3 and Y=t+4
time_step = 100
X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)

print(X_train.shape), print(y_train.shape)

# reshape input to be [samples, time steps, features] which is required for LSTM
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

### Create the Stacked LSTM model
lstm_model=Sequential()
lstm_model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
lstm_model.add(LSTM(50,return_sequences=True))
lstm_model.add(LSTM(50))
lstm_model.add(Dense(1))
lstm_model.compile(loss='mean_squared_error',optimizer='adam')

gru_model=Sequential()
gru_model.add(GRU(50,return_sequences=True,input_shape=(100,1)))
gru_model.add(GRU(50,return_sequences=True))
gru_model.add(GRU(50))
gru_model.add(Dense(1))
gru_model.compile(loss='mean_squared_error',optimizer='adam')

lstm_model.summary()

gru_model.summary()

gru_model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=20,batch_size=64,verbose=1)

lstm_model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=20,batch_size=64,verbose=1)

### Prediction and check performance metrics
lstm_train_predict=lstm_model.predict(X_train)
lstm_test_predict=lstm_model.predict(X_test)
gru_train_predict=gru_model.predict(X_train)
gru_test_predict=gru_model.predict(X_test)

##Transformback to original form
lstm_train_predict = scaler.inverse_transform(lstm_train_predict)
lstm_test_predict = scaler.inverse_transform(lstm_test_predict)
gru_train_predict = scaler.inverse_transform(gru_train_predict)
gru_test_predict = scaler.inverse_transform(gru_test_predict)

### Calculate Mean Squared Error performance metrics
lstm_train_data_rmse = math.sqrt(mean_squared_error(y_train,lstm_train_predict))
lstm_test_data_rmse = math.sqrt(mean_squared_error(ytest,lstm_test_predict))
gru_train_data_rmse = math.sqrt(mean_squared_error(y_train,gru_train_predict))
gru_test_data_rmse = math.sqrt(mean_squared_error(ytest,gru_test_predict))
print('LSTM Train Data RMSE: ', lstm_train_data_rmse)
print('LSTM Test Data RMSE: ', lstm_test_data_rmse)
print('GRU Train Data RMSE: ', gru_train_data_rmse)
print('GRU Test Data RMSE: ', gru_test_data_rmse)

data ={'GRU RMSE Score':gru_test_data_rmse ,'LSTM RMSE Score': lstm_test_data_rmse}
names=list(data.keys())
values=list(data.values())

plt.bar(names,values,color='blue',width=0.2)

plt.xlabel('Neural Network Models')
plt.ylabel('Accuracy Mectric: RMSE')
plt.show()

# plot baseline and predictions
plt.plot(scaler.inverse_transform(df1))
plt.plot(lstm_train_predict, label='LSTM training set')
plt.plot(lstm_test_predict, label='LSTM test set')
plt.plot(gru_train_predict, label ='GRU traning set' )
plt.plot(gru_test_predict, label =' GRU test set')
plt.legend(loc='best')
plt.show()

look_back=100
lstm_trainPredictPlot = np.empty_like(df1)
gru_trainPredictPlot = np.empty_like(df1)
lstm_trainPredictPlot[:, :] = np.nan
gru_trainPredictPlot[:, :] = np.nan
lstm_trainPredictPlot[look_back:len(lstm_train_predict)+look_back, :] = lstm_train_predict
gru_trainPredictPlot[look_back:len(gru_train_predict)+look_back, :] = gru_train_predict
# shift test predictions for plotting
lstm_testPredictPlot = np.empty_like(df1)
gru_testPredictPlot = np.empty_like(df1)
lstm_testPredictPlot[:, :] = np.nan
lstm_testPredictPlot[:, :] = np.nan
lstm_testPredictPlot[len(lstm_train_predict)+(look_back*2)+1:len(df1)-1, :] = lstm_test_predict
gru_testPredictPlot[len(gru_train_predict)+(look_back*2)+1:len(df1)-1, :] = gru_test_predict
# plot baseline and predictions
plt.plot(scaler.inverse_transform(df1))
plt.plot(lstm_trainPredictPlot, label='LSTM train set')
plt.plot(lstm_testPredictPlot, label='LSTM test set')
plt.plot(gru_trainPredictPlot, label = 'GRU train set')
plt.plot(gru_testPredictPlot, label= 'GRU test set')
plt.legend(loc='best')
plt.show()

