import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import tensorflow as tf
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tqdm import tqdm

# Correct the image directory path
image_dir = r'C:/Users/irind/Downloads/tumordataset/tumordata'
no_tumor_images = os.listdir(image_dir + '/no')
yes_tumor_images = os.listdir(image_dir + '/yes')

print("--------------------------------------\n")
print('The length of NO Tumor images is', len(no_tumor_images))
print('The length of Tumor images is', len(yes_tumor_images))
print("--------------------------------------\n")

dataset = []
label = []
img_siz = (128, 128)

# Load NO tumor images
for i, image_name in tqdm(enumerate(no_tumor_images), desc="No Tumor"):
    if image_name.endswith('.jpg'):  # Avoid splitting by '.' as the filename might contain multiple '.'
        image = cv2.imread(image_dir + '/no/' + image_name)
        image = Image.fromarray(image, 'RGB')
        image = image.resize(img_siz)
        dataset.append(np.array(image))
        label.append(0)

# Load YES tumor images
for i, image_name in tqdm(enumerate(yes_tumor_images), desc="Tumor"):
    if image_name.endswith('.jpg'):
        image = cv2.imread(image_dir + '/yes/' + image_name)
        image = Image.fromarray(image, 'RGB')
        image = image.resize(img_siz)
        dataset.append(np.array(image))
        label.append(1)

# Convert to numpy arrays
dataset = np.array(dataset)
label = np.array(label)

print("--------------------------------------\n")
print('Dataset Length:', len(dataset))
print('Label Length:', len(label))
print("--------------------------------------\n")

# Split dataset into training and test sets
print("--------------------------------------\n")
print("Train-Test Split")
x_train, x_test, y_train, y_test = train_test_split(dataset, label, test_size=0.2, random_state=42)
print("--------------------------------------\n")

# Normalize the dataset
print("--------------------------------------\n")
print("Normalizing the Dataset.\n")
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
print("--------------------------------------\n")

# Build the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

print("--------------------------------------\n")
model.summary()
print("--------------------------------------\n")

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
print("--------------------------------------\n")
print("Training Started.\n")
history = model.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1)
print("Training Finished.\n")
print("--------------------------------------\n")

# Plot and save accuracy
plt.plot(history.epoch, history.history['accuracy'], label='accuracy')
plt.plot(history.epoch, history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.savefig(r'C:/Users/irind/Downloads/tumordataset/tumordata/accuracy_plot.png')

# Clear the previous plot
plt.clf()

# Plot and save loss
plt.plot(history.epoch, history.history['loss'], label='loss')
plt.plot(history.epoch, history.history['val_loss'], label='val_loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.savefig(r'C:/Users/irind/Downloads/tumordataset/tumordata/loss_plot.png')

# Model evaluation
print("--------------------------------------\n")
print("Model Evaluation Phase.\n")
loss, accuracy = model.evaluate(x_test, y_test)
print(f'Accuracy: {round(accuracy*100,2)}')
print("--------------------------------------\n")

# Predictions
y_pred = model.predict(x_test)
y_pred = (y_pred > 0.5).astype(int)

print('Classification Report\n', classification_report(y_test, y_pred))
print("--------------------------------------\n")

# Save the model
model.save(r'C:/Users/irind/Downloads/tumordataset/tumordata/model.h5')

# Prediction function
def make_prediction(img_path, model):
    img = cv2.imread(img_path)
    img = Image.fromarray(img)
    img = img.resize((128, 128))
    img = np.array(img)
    input_img = np.expand_dims(img, axis=0)
    res = model.predict(input_img)
    if res > 0.5:
        print("Tumor Detected")
    else:
        print("No Tumor")
    return res

# Test the prediction function
make_prediction(r'C:/Users/irind/Downloads/tumordataset/tumordata/yes/y6.jpg', model)
print("--------------------------------------\n")
make_prediction(r'C:/Users/irind/Downloads/tumordataset/tumordata/no/no8.jpg', model)
print("--------------------------------------\n")
