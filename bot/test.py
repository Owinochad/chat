import numpy as np
from PIL import Image
from keras.models import load_model

# Load the saved Keras model
model = load_model('my_model.h5')

# Function to preprocess the image
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))  # Assuming the model requires input shape (224, 224)
    img_array = np.array(img)  # Convert image to numpy array
    img_array = img_array / 255.0  # Normalize pixel values to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Function to make predictions
def predict_disease(image_path):
    preprocessed_image = preprocess_image(image_path)
    prediction = model.predict(preprocessed_image)
    return prediction

# Function to get disease label based on prediction
def get_disease_info(prediction):
    max_index = np.argmax(prediction)
    if max_index == 0:
        label = "Corn BLIGHT"
    elif max_index == 1:
        label = "Common Rust"
    elif max_index == 2:
        label = "Gray_Leaf_Spot"
    elif max_index == 3:
        label = "Healthy"
    percentage = prediction[0][max_index] * 100
    return label, percentage

# Example usage
image_path = 'Corn_Common_Rust (1).jpg'
prediction = predict_disease(image_path)
label, percentage = get_disease_info(prediction)
print(f"{label}: {percentage:.2f}%")
