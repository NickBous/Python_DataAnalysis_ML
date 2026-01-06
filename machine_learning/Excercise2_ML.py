import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

# Load the dataset
abalone_train = pd.read_csv(
  "abalone_data.csv",
  names=[
    "Length", "Diameter", "Height", "Whole weight", 
    "Shucked weight", "Viscera weight", "Shell weight", "Age"
  ]
)

# Split features and labels
abalone_features = abalone_train.copy()
abalone_labels = abalone_features.pop('Age')

# Convert to numpy arrays
X = abalone_features.to_numpy()
y = abalone_labels.to_numpy()

# Build the model
model = tf.keras.Sequential()
model.add(layers.Dense(units=64, input_shape=(X.shape[1],)))  # First Dense layer with 64 units
model.add(layers.Dense(units=1))  # Second Dense layer with 1 unit for regression

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.MeanSquaredError())

# Train the model
history = model.fit(X, y, epochs=10, verbose=0)

# Print the training history
print(history.history)

# Print model summary
model.summary()
