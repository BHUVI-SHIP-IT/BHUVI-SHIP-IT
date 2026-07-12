import sys
import cv2
import numpy as np
from rembg import remove
from PIL import Image
import io

def prep_photo(input_path, output_path):
    print(f"Loading {input_path}...")
    with open(input_path, "rb") as f:
        input_data = f.read()

    print("Removing background...")
    subject_bytes = remove(input_data)
    
    img = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
    
    # Convert to OpenCV format (numpy array)
    cv_img = np.array(img)
    # PIL is RGBA, OpenCV is BGRA
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGBAstr2BGRA) if hasattr(cv2, 'COLOR_RGBAstr2BGRA') else cv2.cvtColor(cv_img, cv2.COLOR_RGBA2BGRA)
    
    # Extract alpha channel
    b, g, r, a = cv2.split(cv_img)
    
    # Convert to grayscale
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2GRAY)
    
    # Apply CLAHE
    print("Applying CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(gray)
    
    # Re-add alpha channel
    out_img = cv2.merge((cl, cl, cl, a))
    
    # Save
    print(f"Saving to {output_path}...")
    cv2.imwrite(output_path, out_img)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python prep_photo.py <input> <output>")
        sys.exit(1)
    prep_photo(sys.argv[1], sys.argv[2])
