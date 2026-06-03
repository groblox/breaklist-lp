import fitz  # PyMuPDF
from PIL import Image
import cv2
import numpy as np
import os

def extract_images_from_pdf(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Loop through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)

        # Extract the page as a pixmap
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Convert the PIL image to OpenCV format for further processing
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect borders and crop image
        cropped_images = crop_borders(open_cv_image)

        # Save the cropped images
        for idx, cropped in enumerate(cropped_images):
            output_path = os.path.join(output_folder, f"page_{page_num+1}_image_{idx+1}.jpg")
            cv2.imwrite(output_path, cropped)
            print(f"Saved: {output_path}")

    pdf_document.close()

def crop_borders(image):
    # Invert the image (make borders white, background black)
    inverted_image = cv2.bitwise_not(image)

    # Find contours (which should be the borders)
    contours, _ = cv2.findContours(cv2.cvtColor(inverted_image, cv2.COLOR_BGR2GRAY), 
                                   cv2.RETR_EXTERNAL, 
                                   cv2.CHAIN_APPROX_SIMPLE)

    cropped_images = []

    # Loop over the contours
    for contour in contours:
        # Get the bounding box
        x, y, w, h = cv2.boundingRect(contour)

        # Ignore very small contours that are likely noise
        if w > 100 and h > 100:  # Adjust the minimum size as needed
            # Shrink the bounding box to exclude the frame (adjust this value as needed)
            frame_margin = 10  # Adjust this to control how much of the frame you want to exclude
            x_new = x + frame_margin
            y_new = y + frame_margin
            w_new = w - 2 * frame_margin
            h_new = h - 2 * frame_margin + 35  # Extend 20px below the bottom of the frame

            # Ensure we don't go out of bounds
            if y_new + h_new > image.shape[0]:
                h_new = image.shape[0] - y_new

            # Crop the region inside the frame, and extend below by 20px
            cropped_image = image[y_new:y_new+h_new, x_new:x_new+w_new]
            cropped_images.append(cropped_image)

    return cropped_images


# Example usage:
pdf_path = r"C:\Users\rbhei\Downloads\djvu2pdf\farsideGallery1984.pdf"  # Path to your PDF
output_folder = "C:\images"  # Output folder for images

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

extract_images_from_pdf(pdf_path, output_folder)
