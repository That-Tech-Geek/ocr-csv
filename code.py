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
    
    # Initialize lists to store rows and columns
    rows = []
    current_row = []
    last_y = None
    
    for result in results:
        text = result[1]
        box = result[0]
        
        # Use the vertical position (Y coordinate) of the bounding box to determine rows
        y = (box[0][1] + box[2][1]) / 2
        
        if last_y is None or abs(y - last_y) > 10:
            # New row detected
            if current_row:
                rows.append(current_row)
            current_row = [text]
            last_y = y
        else:
            # Continue the current row
            current_row.append(text)
    
    # Append the last row
    if current_row:
        rows.append(current_row)
    
    # Create a DataFrame from the rows
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
