import streamlit as st
import easyocr
import pandas as pd
import tempfile
from PIL import Image
import numpy as np
import io

def ocr_image_to_dataframe(image):
    # Convert PIL Image to NumPy array
    image_np = np.array(image)
    
    # Initialize easyocr reader
    reader = easyocr.Reader(['en'])
    
    # Perform OCR on the image
    results = reader.readtext(image_np, detail=1)
    
    # Initialize list to store rows
    rows = []
    current_row = []
    
    # Process OCR results into rows
    for result in results:
        # Extract text and bounding box
        text = result[1]
        box = result[0]
        
        # Assuming the text is split into columns based on its bounding box
        if len(current_row) > 0 and box[0][1] > current_row[-1][1][1]:
            # If the text starts on a new row
            rows.append([text for text, _ in current_row])
            current_row = []
        current_row.append((text, box))
    
    # Append the last row
    if len(current_row) > 0:
        rows.append([text for text, _ in current_row])
    
    # Create DataFrame with rows and columns
    df = pd.DataFrame(rows)
    
    return df

st.title("Table Image to CSV")

uploaded_image = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # Open image from uploaded file
    image = Image.open(uploaded_image)
    
    # Get DataFrame from OCR
    df = ocr_image_to_dataframe(image)
    
    # Display DataFrame in the app
    st.write("Data extracted from image:")
    st.dataframe(df)
    
    # Save DataFrame to a temporary CSV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
        output_csv_path = tmpfile.name
        df.to_csv(output_csv_path, index=False, header=False)
        
        # Provide a download button for the CSV file
        with open(output_csv_path, "rb") as file:
            st.download_button(
                label="Download CSV",
                data=file,
                file_name="output.csv",
                mime="text/csv"
            )
