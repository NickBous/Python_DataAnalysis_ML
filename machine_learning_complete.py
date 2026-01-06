import tensorflow as tf  
from tensorflow import keras 
import matplotlib.pyplot as pyplot  
import pandas as pd  
import numpy as np  

# Load Fashion MNIST dataset from Keras
fashion_mnist = keras.datasets.fashion_mnist  

# Load the Fashion MNIST dataset into training and testing sets
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

# Print the shape and data type of the training set
print(X_train_full.shape, X_train_full.dtype)
# Print the shape and data type of the labels in the training set
print(y_train_full.shape, y_train_full.dtype)
# Print the shape and data type of the testing set
print(X_test.shape, X_test.dtype)
# Print the shape and data type of the labels in the testing set
print(y_test.shape, y_test.dtype)


# Define class names corresponding to the integer labels
class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]
# Print the mapping of class labels to class names
for label, class_name in enumerate(class_names):
    print(f"Label {label}: {class_name}")




# Iterate through the first 9 images in the training set
for i in range(9):
    # Create subplots with 3 rows and 3 columns, with the current subplot
    # index calculated dynamically
    pyplot.subplot(330 + 1 + i)
    
    # Display the current image using Matplotlib's imshow function, specifying 
    # the colormap as grayscale
    pyplot.imshow(X_train_full[i], cmap=pyplot.get_cmap('gray'))

# Show the plot with all 9 images
pyplot.show()



# Splitting the dataset into validation and training sets
# We allocate 5000 samples for the validation set and the rest for training
X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0

# Splitting the labels into validation and training sets accordingly
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]



# Create a Sequential model
model = keras.models.Sequential()

# Add a Flatten layer to convert each input image (28x28) into a 1D array
model.add(keras.layers.Flatten(input_shape=[28, 28]))
# Add a Dense layer with 300 neurons and ReLU activation function
model.add(keras.layers.Dense(300, activation="relu"))
# Add a second Dense layer with 100 neurons and ReLU activation function
model.add(keras.layers.Dense(100, activation="relu"))
# Add the output Dense layer with 10 neurons (one for each class) and 
# softmax activation function
model.add(keras.layers.Dense(10, activation="softmax"))




# Display model architecture and parameters
model.summary()




# Get the layers of the model
my_layers = model.layers
# Select the first hidden layer
first_hidden_layer = my_layers[1]
# Extract the weights and biases from the first hidden layer
weights, biases = first_hidden_layer.get_weights()



# Compile the model with specified parameters
model.compile(
    # Loss function used for training, suitable for integer labels
    loss="sparse_categorical_crossentropy", 
    # Stochastic Gradient Descent optimizer for updating model parameters
    optimizer="sgd",  
    # Metric to evaluate model performance during training and testing
    metrics=["accuracy"]  
)



# Training the model using the fit method
history = model.fit(
    X_train,            # Training data features
    y_train,            # Training data labels
    epochs=30,          # Number of training epochs
    validation_data=(X_valid, y_valid)  # Validation data for monitoring model performance
)



# Create a DataFrame from training history and plot it
pd.DataFrame(history.history).plot(figsize=(8, 5))  
# Add grid lines to the plot
pyplot.grid(True)  
# Set the vertical range of the plot to [0-1]
pyplot.gca().set_ylim(0, 1)  
# Set the title of the plot
pyplot.title('Training History') 


# The method returns the loss value and any additional metrics 
# specified during model compilation.
model.evaluate(X_test, y_test)


# Selecting new instances for prediction
X_new = X_test[:3]
# Using the trained model to predict probabilities for the new instances
y_proba = model.predict(X_new)
# Printing the predicted probabilities rounded to two decimal places
print(y_proba.round(2))




# 'y_proba' contains predicted probabilities for each class,
# 'class_names_idx' stores the index of the class with the highest 
# probability for each prediction.
class_names_idx = np.argmax(y_proba, axis=1)
# 'class_names' is the list containing the names of all classes in the dataset.
# 'result' is a list that stores the class names corresponding to 
# the predicted class indices.
result = [class_names[i] for i in class_names_idx]
# Print the extracted class names
print(result)
