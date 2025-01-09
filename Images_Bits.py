import os
import numpy as np
from PIL import Image
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

def image_to_bitlist(img):

    """
    Return a image as a list of bits in hexadecimal
    """

    # Convert the image to gray scale
    img = img.convert("1")

    # Obtain the size of the image
    width, height = img.size

    # Make a list of bits
    bit_list = []

    # Go trough every pixel in the image
    for y in range(height):
        for x in range(width):
            # Obtener el valor de color del píxel (in binary)
            pixel_value = img.getpixel((x, y))

            # Convertir el valor a binario y quitar el prefijo '0b'
            pixel_bits = bin(pixel_value)[2:].zfill(8)  # Asegura que tenga 8 bits

            # Add the bits to the list and convert the bit in hexadecimal
            bit_list.append(binary_to_hexa(pixel_bits))

    return bit_list

def binary_to_hexa(binario):

    decimal = int(binario, 2) ##Convert binario to decimal with int. Int can use 2 arguments, the number, and the base of that number
    hexa = hex(decimal)
    return hexa


def hex_to_image(hex_list, width, height):
    # Unir todos los valores hexadecimales en una sola cadena
    hex_string = ''.join(hex_list)

    # Convertir la cadena hexadecimal en bytes
    image_data = bytes.fromhex(hex_string)

    # Crear una imagen a partir de los bytes
    image = Image.open(io.BytesIO(image_data))

    # Verificar que la imagen tiene las dimensiones correctas
    image = image.resize((width, height))

    # Mostrar la imagen
    image.show()

miniatures = resizeList(load_images((select_folder())), 128, 64)

bit_list = image_to_bitlist(select_image())

# Mostrar los primeros 100 bits de la lista como ejemplo
print(bit_list)

cosa = [
    0x00, 0x25, 0x55, 0x55, 0x55, 0x04, 0xa4, 0x09, 0x00, 0x2a, 0xaa, 0xaa, 0xaa, 0xaa, 0x49, 0x55,
    0x55, 0x08, 0x09, 0x55, 0x54, 0xa1, 0x51, 0x44, 0x55, 0x44, 0x95, 0x55, 0x55, 0x29, 0x24, 0x12,
    0x00, 0xa2, 0xa4, 0x08, 0xaa, 0x94, 0x40, 0x11, 0x00, 0x12, 0x40, 0x55, 0x52, 0xa5, 0x55, 0xa4,
    0x55, 0x14, 0x49, 0x52, 0x04, 0x41, 0x15, 0x44, 0x55, 0x4a, 0xaf, 0x55, 0x4a, 0xaa, 0x94, 0x48,
    0x02, 0x49, 0x22, 0x48, 0xa9, 0x24, 0x00, 0x11, 0x00, 0x95, 0x51, 0x52, 0xaa, 0x55, 0x52, 0x92,
    0xa9, 0x24, 0x94, 0xa5, 0x11, 0x48, 0xa5, 0x44, 0x56, 0xd5, 0x5d, 0x49, 0x25, 0x54, 0xaa, 0x49,
    0x24, 0x92, 0x49, 0x12, 0x45, 0x10, 0x10, 0x11, 0x29, 0x55, 0xa5, 0x00, 0x15, 0x55, 0x14, 0xa4,
    0x92, 0x49, 0x24, 0xa4, 0x91, 0x42, 0xa5, 0x4a, 0x44, 0x55, 0x5a, 0x80, 0x12, 0xaa, 0xea, 0x52,
    0x49, 0x24, 0x92, 0x12, 0x4a, 0x8a, 0x14, 0xa4, 0x92, 0x8a, 0x4a, 0x80, 0x0a, 0x4a, 0x29, 0x14,
    0x24, 0x52, 0x49, 0x49, 0x25, 0x4a, 0x42, 0x52, 0x48, 0x51, 0x24, 0x08, 0x05, 0x55, 0xa4, 0xa2,
    0x91, 0x09, 0x54, 0xa4, 0x90, 0x15, 0x29, 0x09, 0x25, 0x24, 0xaa, 0x9e, 0x12, 0xaa, 0xb2, 0x54,
    0x44, 0xa4, 0x8a, 0x52, 0x12, 0xca, 0x44, 0xa4, 0x10, 0x92, 0x90, 0x77, 0x08, 0xaa, 0xa9, 0x09,
    0x2a, 0x02, 0x20, 0x08, 0xd2, 0xa8, 0x11, 0x51, 0x44, 0x4a, 0x4a, 0xdd, 0x05, 0x28, 0x84, 0xa2,
    0x95, 0x50, 0x95, 0x49, 0x4d, 0x55, 0x4a, 0x04, 0x22, 0x31, 0x23, 0x7b, 0x82, 0x95, 0x52, 0x14,
    0x6a, 0xae, 0xd4, 0xa2, 0x95, 0x54, 0xb6, 0xf5, 0xad, 0x6c, 0x09, 0xae, 0x0d, 0x6a, 0xad, 0xd5,
    0xaa, 0xb5, 0x5a, 0xb2, 0x55, 0x2a, 0xaa, 0x90, 0x35, 0x7a, 0x2f, 0xfa, 0x0a, 0xaa, 0xb5, 0x5a,
    0x55, 0x55, 0xaa, 0xa9, 0x2a, 0xa5, 0x00, 0x90, 0x02, 0x17, 0x7d, 0x58, 0x20, 0x02, 0x00, 0x00,
    0xaa, 0xaa, 0xad, 0x2a, 0xa9, 0x22, 0x6f, 0x68, 0x5c, 0x61, 0x17, 0xe5, 0xdb, 0x59, 0xd5, 0x6a,
    0x55, 0x56, 0xd5, 0x29, 0x54, 0x29, 0x10, 0x80, 0x60, 0x85, 0xea, 0x84, 0x24, 0xa4, 0x25, 0x12,
    0xaa, 0xaa, 0xaa, 0xc2, 0x51, 0x54, 0x8a, 0x2b, 0xb7, 0xdf, 0x73, 0x11, 0x40, 0x02, 0x88, 0x44,
    0x55, 0x5a, 0xaa, 0x9d, 0xa4, 0x25, 0x21, 0x43, 0xdb, 0x75, 0xd0, 0x00, 0x2a, 0xa8, 0x42, 0x90,
    0xaa, 0x55, 0x54, 0x04, 0x52, 0x54, 0x9d, 0x58, 0x7d, 0xbf, 0x60, 0x00, 0x12, 0xab, 0x54, 0x45,
    0x42, 0xaa, 0x41, 0x55, 0x4b, 0x6a, 0x92, 0x27, 0xab, 0xd5, 0x00, 0x00, 0x49, 0x2a, 0xaa, 0xb4,
    0xaa, 0x80, 0x94, 0x95, 0x4a, 0x4a, 0x80, 0x12, 0xde, 0xff, 0x60, 0x00, 0x2a, 0xa4, 0xaa, 0xab,
    0x10, 0x54, 0x0a, 0x29, 0x4a, 0xa5, 0x40, 0x02, 0x6b, 0x55, 0xb0, 0x00, 0x15, 0x53, 0x55, 0x5a,
    0x44, 0x02, 0xa1, 0x95, 0x52, 0x8a, 0x40, 0x04, 0x4d, 0xee, 0xa8, 0x00, 0x55, 0x15, 0x5a, 0xaa,
    0x01, 0x59, 0x3d, 0x29, 0x48, 0x92, 0x80, 0x01, 0xb7, 0x5b, 0xbc, 0x00, 0x2a, 0xaa, 0xa1, 0x55,
    0x48, 0x85, 0xa6, 0xad, 0x54, 0x85, 0x40, 0x00, 0xdd, 0xf6, 0xb0, 0x00, 0xa9, 0x2b, 0x54, 0x56,
    0x12, 0x2a, 0x50, 0x29, 0x0a, 0x75, 0x20, 0x14, 0x12, 0x98, 0x59, 0x46, 0xa5, 0x2a, 0xa1, 0x0b,
    0x45, 0x55, 0xa5, 0x2a, 0xa0, 0x04, 0x00, 0x4a, 0x8d, 0x40, 0x02, 0xb5, 0x54, 0x55, 0x4a, 0xa8,
    0x29, 0x6a, 0xa0, 0x51, 0x00, 0x28, 0x6b, 0x24, 0x00, 0x00, 0x0a, 0x95, 0x55, 0x15, 0x2a, 0xa5,
    0xaa, 0xad, 0x4a, 0x55, 0x40, 0x03, 0x4a, 0x80, 0x00, 0x00, 0x12, 0xaa, 0xaa, 0x8a, 0x8a, 0xa2,
    0x55, 0x55, 0xa4, 0x52, 0x80, 0x08, 0x00, 0x00, 0x00, 0x00, 0x0a, 0xaa, 0xa4, 0x20, 0x25, 0x4a,
    0x49, 0x55, 0x41, 0x09, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x55, 0x55, 0x55, 0x0b, 0x55, 0x2d,
    0x54, 0xaa, 0xa8, 0xe4, 0x80, 0x00, 0x4a, 0xa8, 0x00, 0x00, 0xa4, 0xaa, 0x95, 0x55, 0x55, 0x55,
    0x55, 0x55, 0x46, 0x32, 0x80, 0x23, 0x2a, 0xb0, 0x00, 0x02, 0x12, 0xaa, 0xa9, 0x02, 0xaa, 0xaa,
    0x4a, 0x95, 0x4b, 0xa5, 0x40, 0x14, 0xa5, 0x2a, 0x00, 0x09, 0xaa, 0xaa, 0xa5, 0x68, 0xaa, 0x29,
    0x24, 0xaa, 0xa8, 0x94, 0x96, 0xb3, 0x4a, 0x9b, 0xc0, 0x7a, 0x55, 0x4a, 0xaa, 0xa2, 0x12, 0x94,
    0xaa, 0x95, 0x46, 0x29, 0x4a, 0x99, 0x2a, 0xa6, 0xaf, 0xa9, 0x44, 0xa9, 0x55, 0x58, 0xa4, 0x41,
    0x25, 0x55, 0x50, 0x2a, 0x4a, 0x8a, 0x95, 0x5f, 0x6e, 0xf5, 0x2a, 0x55, 0x55, 0x55, 0x08, 0x10,
    0x94, 0x52, 0x81, 0x29, 0x4d, 0x6a, 0x55, 0x2b, 0x57, 0xa2, 0x92, 0x95, 0x55, 0x55, 0x52, 0x06,
    0x53, 0x2a, 0x64, 0x14, 0xa9, 0x44, 0x92, 0xbd, 0xfa, 0xca, 0x54, 0xaa, 0xaa, 0xaa, 0xa9, 0xaa,
    0x08, 0xa5, 0x20, 0x94, 0xa9, 0x69, 0x4a, 0x4a, 0x17, 0x65, 0x4a, 0xaa, 0xaa, 0xaa, 0x95, 0x55,
    0xaa, 0x52, 0x84, 0x0a, 0x4b, 0x4a, 0x95, 0x50, 0x4a, 0x00, 0x21, 0x09, 0x54, 0x00, 0x48, 0x24,
    0x45, 0x4a, 0xa0, 0x95, 0x31, 0x49, 0x29, 0x48, 0xa0, 0x0a, 0xac, 0xaa, 0xaa, 0xad, 0x57, 0x52,
    0x29, 0x29, 0x44, 0x09, 0x49, 0x2a, 0x85, 0x54, 0x55, 0x01, 0x52, 0x55, 0x55, 0x2a, 0xa9, 0x4a,
    0x94, 0x94, 0xa0, 0x44, 0x55, 0x25, 0x32, 0xa0, 0x12, 0x00, 0x0a, 0x95, 0x52, 0x94, 0x94, 0x92,
    0x42, 0x42, 0x41, 0x03, 0x2a, 0x12, 0x4a, 0x9a, 0x49, 0x44, 0x52, 0x49, 0x54, 0xa5, 0x4a, 0xa9,
    0x2a, 0xa9, 0x24, 0x24, 0x95, 0x54, 0x11, 0x48, 0x09, 0x01, 0x05, 0x2a, 0x95, 0x12, 0x52, 0x44,
    0x44, 0x15, 0x40, 0x00, 0x09, 0x49, 0x54, 0x2a, 0x14, 0xa0, 0xa0, 0x52, 0x52, 0xa5, 0x09, 0x29,
    0x12, 0xa0, 0x80, 0x80, 0x84, 0xa0, 0x92, 0xa1, 0x02, 0x50, 0x14, 0x09, 0x29, 0x12, 0xa5, 0x44,
    0x49, 0x15, 0x22, 0x11, 0x51, 0x4a, 0x4a, 0x14, 0x01, 0x20, 0xa1, 0x20, 0x84, 0xa4, 0x28, 0xa9,
    0x24, 0x48, 0x88, 0x02, 0x00, 0x12, 0x51, 0xf1, 0x8c, 0x48, 0x17, 0x8a, 0x2a, 0x11, 0x05, 0x10,
    0x49, 0x25, 0x40, 0x00, 0x95, 0x25, 0x09, 0x5e, 0xf4, 0xa4, 0x18, 0x01, 0x01, 0x4a, 0x51, 0x45,
    0x22, 0x48, 0x20, 0x22, 0x48, 0x88, 0xa1, 0x65, 0x54, 0x13, 0x21, 0x54, 0xa0, 0x40, 0x88, 0x28,
    0x49, 0x25, 0x40, 0x81, 0x12, 0x22, 0x2a, 0x2d, 0xb4, 0xa1, 0x44, 0xa1, 0x15, 0x2a, 0x25, 0x42,
    0x02, 0x10, 0x02, 0x00, 0x21, 0x14, 0x84, 0x50, 0x04, 0x06, 0x8a, 0x84, 0x40, 0x00, 0x00, 0x10,
    0x50, 0xa5, 0x40, 0x15, 0x4a, 0x42, 0x50, 0x02, 0x00, 0xa5, 0x12, 0x01, 0x15, 0x2a, 0xaa, 0x8a,
    0x04, 0x12, 0x20, 0x04, 0x00, 0x29, 0x0a, 0x90, 0xa4, 0x11, 0x20, 0x48, 0x88, 0x00, 0x00, 0x20,
    0x22, 0x48, 0x80, 0xa9, 0x55, 0x04, 0x40, 0x24, 0x11, 0x40, 0x00, 0x02, 0x20, 0xa9, 0x0a, 0x15,
    0x08, 0x04, 0x00, 0x02, 0x00, 0xa9, 0x2a, 0x42, 0x82, 0x08, 0x00, 0x01, 0x02, 0x00, 0x00, 0x40,
    0x41, 0x50, 0x85, 0x50, 0x12, 0x00, 0x00, 0x10, 0x50, 0x41, 0x12, 0x14, 0x48, 0x92, 0x48, 0x04,
    0x00, 0x04, 0x20, 0x04, 0x80, 0xaa, 0xa5, 0x04, 0x04, 0x84, 0x40, 0x80, 0x22, 0x40, 0x00, 0x80,
    0x04, 0x90, 0x8a, 0x90, 0x08, 0x00, 0x00, 0x21, 0x20, 0x00, 0x02, 0x12, 0x08, 0x04, 0x00, 0x00
 ]

print(len(cosa))

#Se debe convertir en monochrome

#for i in range(len(miniatures)):
 #   print(bit_list)

#save_images(miniatures, r"C:\Users\Alejandro\Desktop\redimensionadas")