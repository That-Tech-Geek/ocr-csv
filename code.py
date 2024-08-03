import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import io

# Function to perform OCR on the uploaded image and convert to CSV
def ocr_image_to_csv(image):
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(image)
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Extract rows from the lines
    rows = [line.split() for line in lines if line.strip()]
    
    # Create a DataFrame from the rows
    df = pd.DataFrame(rows)
    
    return df

# Streamlit UI
st.title('Image to CSV Converter')
st.write('Upload an image of a table to convert it to a CSV file.')

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open the uploaded image
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Processing...")
    
    # Convert the image to CSV
    df = ocr_image_to_csv(image)
    
    # Display the DataFrame
    st.dataframe(df)
    
    # Create a CSV download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='output.csv',
        mime='text/csv'
    )
