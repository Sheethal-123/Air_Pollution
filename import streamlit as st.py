import streamlit as st
import requests

# Set up the Streamlit app
st.title("Real-Time Pollution Data Classification")
st.write("Provide input data to get real-time classification results.")

# Input form
with st.form("prediction_form"):
    quality_id = st.number_input("Quality ID", min_value=1, step=1)
    factor_id = st.number_input("Factor ID", min_value=1, step=1)
    pollutant_id = st.number_input("Pollutant ID", min_value=1, step=1)
    temperature = st.number_input("Temperature (°C)")
    humidity = st.number_input("Humidity (%)")
    proximity_to_industry = st.number_input("Proximity to Industry (km)")
    population_density = st.number_input("Population Density")
    pm2_5 = st.number_input("PM2.5 Level")
    pm10 = st.number_input("PM10 Level")
    no2 = st.number_input("NO2 Level")
    so2 = st.number_input("SO2 Level")
    co = st.number_input("CO Level")

    submit = st.form_submit_button("Classify")

# FastAPI endpoint
API_URL = "http://localhost:8000/predict"  # Replace with your actual FastAPI endpoint

# Submit data to the FastAPI endpoint
if submit:
    input_data = {
        "quality_id": int(quality_id),
        "factor_id": int(factor_id),
        "pollutant_id": int(pollutant_id),
        "Temperature_C": float(temperature),
        "Humidity_percent": float(humidity),
        "Proximity_to_Industry_km": float(proximity_to_industry),
        "Population_Density": float(population_density),
        "PM2_5": float(pm2_5),
        "PM10": float(pm10),
        "NO2": float(no2),
        "SO2": float(so2),
        "CO": float(co),
    }

    try:
        # Make the POST request to FastAPI
        response = requests.post(API_URL, json=input_data)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        prediction = response.json()

        # Display the prediction result
        st.write("### Classification Result")
        st.json(prediction)
    except Exception as e:
        st.error(f"An error occurred: {e}")
