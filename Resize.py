import os
import numpy as np
from PIL import Image
import math
from tkinter import Tk, filedialog, messagebox

def load_images(route):
    """
    Loads images from a folder, converts them to numpy arrays, and returns them as a list.
    route -> Absolute path where the images are located.
    images -> List of numpy ndarray arrays.
    """
    images = []
    directory = os.fsencode(route)
    os.chdir(route)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith((".jpg", ".jpeg")):
            img = Image.open(filename)
            img.load()
            data = np.asarray(img, dtype="uint8")
            print(data.shape)
            images.append(data)
            continue
        else:
            continue
    print("Loaded", len(images), "images\n")
    return images


def save_images(images, route):
    """
    Saves a list of images (as numpy arrays) to the specified folder.
    images -> List of numpy ndarray images.
    route -> Absolute path where the images will be saved.
    """

    if not os.path.exists(route):
        print("Put a current directory")        # Create the directory if it doesn't exist
        return 0

    for idx, img_data in enumerate(images):
        # Convert the numpy array back to an image
        img = Image.fromarray(img_data)

        # Define the file name for the saved image
        filename = f"image_{idx + 1}.jpg"
        file_path = os.path.join(route, filename)

        # Save the image
        img.save(file_path)

    print(f"Saved {len(images)} images to {route}\n")


def resizeList(A, w, h):
    """
    Resizes a list of images to the specified width and height using the nearest neighbor method.
    """
    for i in range(len(A)):
        A[i] = nearest_neighbor(A[i], w, h)
    return A


def nearest_neighbor(A, w, h):
    """
    Resizes image A to the specified width and height using the nearest neighbor algorithm.
    """
    height, width = A.shape[0], A.shape[1]
    new_image = [[A[int(height * y / h)][int(width * x / w)]
                  for x in range(w)] for y in range(h)]
    return np.array(new_image)


def select_folder():
    """
    Opens a window to select a folder, which should contain the images
    """
    Tk().withdraw()  # Hides the root window
    return filedialog.askdirectory(title="Select a folder")

def select_image():
    """
    Opens a window where you can select an image. It uses askopenfilename instead of askopenfile to avoid errors.
    """
    Tk().withdraw()  # Hide the root window
    return Image.open(filedialog.askopenfilename(title="Select an image",
                                                 filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]))


miniatures = resizeList(load_images((select_folder())), 128, 64)

    # It is recommended to adjust the dimensions of the source images and the pixels of the resulting image
    # For example, for a picture of 2500 x 1875, use w:25, h:19 for 100 pixels.
    # For square pictures, w=h

save_images(miniatures, r"C:\Users\Alejandro\Desktop\redimensionadas")

# Este es el que tiene mayor definicion la imagen, pero se ven menos los colores
# Se logra definir la imagen
# utiliza la suma de la distancias L1 y L2. L2 = distancia de color, L1 = luminancia brillo de color

