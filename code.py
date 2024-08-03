import streamlit as st
import easyocr
import pandas as pd
import tempfile
from PIL import Image
import io

def ocr_image_to_dataframe(image):
    # Initialize easyocr reader
    reader = easyocr.Reader(['en'])
    
    # Perform OCR on the image
    results = reader.readtext(image, detail=1)
    
    # Process OCR results into rows
    rows = []
    for result in results:
        # Extract text
        text = result[1]
        # Split text into columns based on spaces
        columns = text.split()
        rows.append(columns)
    
    # Create a DataFrame with the rows and columns
    df = pd.DataFrame(rows)
    
    return df

st.title("OCR to DataFrame")

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
