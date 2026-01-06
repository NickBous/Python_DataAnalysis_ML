import helper
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

# Load the dataset
df = pd.read_csv('TSLA.csv')
print(df.columns)

# Use only the 'Open' column for prediction
df = df['Open'].values
df = df.reshape(-1, 1)

# Split into training and testing sets (80% training, 20% testing)
dataset_train = np.array(df[:int(df.shape[0] * 0.8)])
dataset_test = np.array(df[int(df.shape[0] * 0.8):])

# Scale the values to the range (0, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
dataset_train = scaler.fit_transform(dataset_train)
dataset_test = scaler.transform(dataset_test)

# Create train/test datasets using helper function
x_train, y_train = helper.create_dataset(dataset_train)
x_test, y_test = helper.create_dataset(dataset_test)

# Reshape datasets to 3D (samples, timesteps, features)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Build the LSTM model
model = Sequential()
# First LSTM layer (returns sequences)
model.add(LSTM(units=4, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
# Second LSTM layer (returns single output)
model.add(LSTM(units=4, return_sequences=False))
model.add(Dropout(0.2))
# Output layer with single neuron for regression task
model.add(Dense(units=1))

# Compile the model
model.compile(optimizer="adam", loss="mean_squared_error")

# Train the model
model.fit(x_train, y_train, epochs=5, batch_size=16, verbose=0)

# Make predictions on the test data
y_pred = model.predict(x_test)

# Print the last column of the predictions
print(y_pred[:, -1] if y_pred.ndim > 1 else y_pred[-1])

# Print the model summary
model.summary()
