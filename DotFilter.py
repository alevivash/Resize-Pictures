import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def apply_dithering(image_path, output_path, threshold=128):
    """
    Convert an image to a monochrome (black and white) image with dithering.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        threshold (int): Threshold for binarization (0-255).

    Returns:
        None
    """
    # Load the image and convert to grayscale
    img = Image.open(image_path).convert("L")
    img_array = np.array(img, dtype=np.float32)

    # Get image dimensions
    height, width = img_array.shape

    # Apply Floyd-Steinberg dithering
    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x]
            new_pixel = 255 if old_pixel > threshold else 0
            img_array[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            # Distribute the quantization error
            if x + 1 < width:
                img_array[y, x + 1] += quant_error * 7 / 16
            if y + 1 < height:
                if x > 0:
                    img_array[y + 1, x - 1] += quant_error * 3 / 16
                img_array[y + 1, x] += quant_error * 5 / 16
                if x + 1 < width:
                    img_array[y + 1, x + 1] += quant_error * 1 / 16

    # Convert back to uint8 and save the result
    img_dithered = Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))
    img_dithered.save(output_path)

    # Display the result
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(img, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Dithered Image")
    plt.imshow(img_dithered, cmap="gray")
    plt.axis("off")

    plt.show()

# Example usage
input_image = "image_1.jpg"  # Replace with the path to your image
output_image = "output_dithered.jpg"
apply_dithering(input_image, output_image)
