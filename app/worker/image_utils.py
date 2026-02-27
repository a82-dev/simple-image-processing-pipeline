import os

from PIL import Image, ImageFilter

from app.core.config import settings


def apply_heavy_filter(filename: str) -> str:
    """
    Takes an image, creates a grayscale version, and saves it.
    """
    input_path = os.path.join(settings.UPLOAD_DIR, filename)
    output_filename = f"processed_{filename}"
    output_path = os.path.join(settings.PROCESSED_DIR, output_filename)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Image {filename} not found.")

    with Image.open(input_path) as img:
        # Convert to Grayscale
        gray_img = img.convert("L")
        # Apply an edge enhancement filter
        final_img = gray_img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        final_img.save(output_path)

    return output_filename
