
from PIL import Image as PILImage

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import  Model

from PIL import Image
import pickle
import numpy as np

# Ham tao model
def get_extract_model():
    vgg16_model = VGG16(weights="imagenet")
    extract_model = Model(inputs=vgg16_model.inputs, outputs = vgg16_model.get_layer("fc1").output)
    return extract_model

# Ham tien xu ly, chuyen doi hinh anh thanh tensor
def image_preprocess(img):
    img = img.resize((224,224))
    img = img.convert("RGB")
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

# def extract_vector(model, image_path):
#     print("Xu ly : ", image_path)
#     img = Image.open(image_path)
#     img_tensor = image_preprocess(img)

#     # Trich dac trung
#     vector = model.predict(img_tensor)[0]
#     # Chuan hoa vector = chia chia L2 norm (tu google search)
#     vector = vector / np.linalg.norm(vector)
#     return vector
def extract_vector(model, image_file):
    img = PILImage.open(image_file)
    img = img.resize((224, 224))
    img_tensor = image_preprocess(img)

    # Trich dac trung
    vector = model.predict(img_tensor)[0]
    # Chuan hoa vector = chia chia L2 norm (tu google search)
    vector = vector / np.linalg.norm(vector)
    return vector

# # Dinh nghia anh can tim kiem
# search_image = "test_images/317998465_1228741551326443_6125795881385636226_n.jpg"
#search item by image
def search_item_by_image(search_image):
    model = get_extract_model()
    search_vector = extract_vector(model, search_image)
    vectors = pickle.load(open("ml/vectors.pkl","rb"))
    paths = pickle.load(open("ml/paths.pkl", "rb"))
    # Tinh khoang cach tu search_vector den tat ca cac vector
    distance = np.linalg.norm(vectors - search_vector, axis=1)
    # Sap xep va lay ra K vector co khoang cach ngan nhat
    K = 9
    ids = np.argsort(distance)[:K]
    # Tao oputput
    nearest_image = [(paths[id], distance[id]) for id in ids]
    return nearest_image

# print(search_item_by_image(search_image))