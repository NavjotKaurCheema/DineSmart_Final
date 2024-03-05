import streamlit as st
from pathlib import Path
import google.generativeai as genai

from dotenv import load_dotenv
import os

load_dotenv()  

from api_key import api_key

genai.configure(api_key=api_key)

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]


system_prompt = """
As a highly skilled medical practitioner and nutritionlist specializing in image analysis,you are tasked with examining food images for a renowned hospital.Your expertise is crucial in identifying whether given image of food item is ideal for patient suffering with given disease
Your Responsibilities include:
1.Person disease:Ask user the disease person is suffering from.Remember them and list them out in your further response
2.Results:Give output as yes or no to specify person should eat given food item or not.If he can eat output-"Yes!you can eat this" else "No!You can't eat this"
3.Disclamer:Accompany your analysis with a disclamer :"Consult with a Doctor before making any decisions."
4.Nutrients List:Document all Nutrients present in given food item.Clearly articulate these findings in structured format.
5.Detailed analysis:Thoroughly analyze each image ,focusing on nutrients of given food item and hazadous given food item can have on patients health for particular disease provided by patient.Keep this detailed analysis hidden Make a kind of button which user can press to get more details about food item.


Important notes:
1.Scope of response:only respond if image contains food item else give error for any other image other then food item.
2.Clarity of image:In case where the image quality impedes clear analysis,note that certain aspects are "Unable to be determined based on provided image."
3.Your insights are invaluable in guuiding clinical and nutritional decisions.Please proceed with the analysis,adhering to the structured approach outline above.
4.Your way of representing results should always remain same
5.Always show Detailed analysis and Nutrients List only if user click button never before that.


Please always provide me an output response with these 3 bold sub headings- 
Subheading 1-
"Person Disease"
Subheading 2-
"Results"
Subheading 3-
"Disclamer"

Detailed analysis:
Show details of given image here
Nutrients List:
show this in bullets list format  .also always include the percentage of nutrients based on your analysis of quantity in given image.This list should always remain same for specific image
"""

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

st.set_page_config(page_title="Dine_Smart", page_icon=":robot")

# Custom styling for the app
custom_css = """
body {
    background-color: #e6ffe6; /* light green */
    font-family: 'Helvetica', 'Arial', sans-serif;
}
h1 {
    color: #0047ab;
    font-weight: bold;
    margin-bottom: 20px;
}
h2 {
    color: #333;
    font-weight: bold;
    margin-bottom: 10px;
}
h3 {
    color: #777;
    font-weight: normal;
    margin-bottom: 10px;
}
p {
    color: #666;
    font-weight: normal;
    line-height: 1.5em;
    margin-bottom: 20px;
}
ul {
    list-style-position: inside;
    padding: 0;
    margin: 0;
}
li {
    padding-bottom: 5px;
}
a {
    color: #0047ab;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
.button {
    background-color: #0047ab;
    color: #fff;
    padding: 10px 15px;
    border-radius: 5px;
    text-decoration: none;
}
.button:hover {
    background-color: #00397b;
}
.image-container {
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 20px;
}
.image {
    width: 100%;
    height: auto;
}
.results-container {
    background-color: #fff;
    padding: 20px;
    margin-bottom: 20px;
}
.nutrient-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
}
.nutrient-item {
    padding-bottom: 5px;
}
"""

# Apply custom CSS to the app
st.write(f'<style>{custom_css}</style>', unsafe_allow_html=True)

# Add a logo
st.image("logo.png", width=200)

# Page title and description
st.title("DineSmart 🍽️💡")
st.subheader("Your Personalized Health Navigator for Smart Dining Choices")

# File uploader
uploaded_file = st.file_uploader("Upload the food image for analysis", type=["png", "jpg", "jpeg"])

# Display uploaded image
if uploaded_file:
    st.image(uploaded_file, width=300, caption="Uploaded Food Item")

# Disease input field
person_diseases = st.multiselect("Enter the diseases you are suffering from:",
                                 [
    "Tuberculosis",
    "High Blood Pressure",
    "Low Blood Pressure",
    "Common Cold",
    "fever",
    "Corona",
    "Cough",
    "flu",
    "Heart Disease",
    "High Cholestrol"
    "headache",
    "Diabetes",
    "Malaria",
    "Dengue",
    "HIV/AIDS",
    "Hepatitis B",
    "Hepatitis C",
    "Diarrhea",
    "Pneumonia",
    "Typhoid",
    "Leprosy",
    "Kala-azar",
    "Japanese encephalitis",
    "Chikungunya",
    "Filariasis",
    "Scabies",
    "Measles",
    "Rubella",
    "Mumps",
    "Whooping cough",
    "Tetanus",
    "Diphtheria",
    "Polio",
    "Rotavirus",
    "Cholera",
    "Typhoid fever",
    "Hepatitis A",
    "Rabies",
    "Japanese encephalitis",
    "Dengue fever",
    "Chikungunya",
    "Zika virus",
    "Crimean-Congo hemorrhagic fever",
    "Nipah virus",
    "Kyasanur Forest disease",
    "Scrub typhus",
    "Leptospirosis",
    "Plague",
    "Anthrax",
    "Brucellosis",
    "Glanders",
    "Melioidosis",
    "Q fever",
    "Rift Valley fever",
    "West Nile virus",
    "Yellow fever",
    "Dengue hemorrhagic fever",
    "Severe dengue",
    "Chikungunya fever",
    "Zika virus infection",
    "Japanese encephalitis",
])

# Submit button
submit_button = st.button("Generate the analysis")

# Generate analysis when submit button is clicked
if submit_button:
    image_data = uploaded_file.getvalue()

    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]

    prompt_parts = [
        "Person disease:",
        ", ".join(person_diseases),
        image_parts[0],
        system_prompt,
    ]

    response = model.generate_content(prompt_parts)
    if response:
        st.title("Here is the analysis based on your image")

        # Show the results (excluding the nutrients list)
        results = response.text.split("Detailed analysis:")[0]
        st.write(results)

        # Add a button to show the detailed analysis
        detailed_analysis_button = st.expander(label="Show Detailed Analysis")
        with detailed_analysis_button:
            if "Detailed analysis:" in response.text:
                st.write(response.text.split("Detailed analysis:")[1].split("Nutrients List:")[0])
            else:
                st.write("Detailed analysis not available for this image.")

        # Add a button to show the nutrients list
        nutrients_list_button = st.expander(label="Show Nutrients List")
        with nutrients_list_button:
            st.write(response.text.split("Nutrients List:")[1])