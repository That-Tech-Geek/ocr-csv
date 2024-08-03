import streamlit as st
import easyocr
import pandas as pd
from io import StringIO

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

def main():
    st.title("OCR Image Text Extraction")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Process the uploaded image
        df = ocr_image_to_dataframe(uploaded_file)
        
        # Display DataFrame
        st.write("Extracted Text:")
        st.dataframe(df)
        
        # Convert DataFrame to CSV format for download
        csv = df.to_csv(index=False, header=False)
        st.download_button(label="Download CSV", data=csv, file_name="output.csv", mime="text/csv")

if __name__ == "__main__":
    main()
