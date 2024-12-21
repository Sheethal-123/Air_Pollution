from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# Load the saved model
model = joblib.load('final_model.pkl')  # Make sure this model expects the correct columns

# Initialize the FastAPI app
app = FastAPI()

# Define the input schema for prediction
class PredictionRequest(BaseModel):
    quality_id: int
    factor_id: int
    pollutant_id: int
    Temperature_C: float
    Humidity_percent: float
    Proximity_to_Industry_km: float
    Population_Density: float
    PM2_5: float
    PM10: float
    NO2: float
    SO2: float
    CO: float

# Define the prediction endpoint
@app.post("/predict")
def predict(request: PredictionRequest):
    print(f"Received data: {request}")  # Log the received request for debugging

    # Convert input data into a DataFrame
    input_data = pd.DataFrame([{
        "quality_id": request.quality_id,
        "factor_id": request.factor_id,
        "pollutant_id": request.pollutant_id,
        "Temperature_C": request.Temperature_C,
        "Humidity_%": request.Humidity_percent,  # Ensure correct column name
        "Proximity_to_Industry_km": request.Proximity_to_Industry_km,
        "Population_Density": request.Population_Density,
        "PM2.5": request.PM2_5,  # Ensure correct column name
        "PM10": request.PM10,
        "NO2": request.NO2,
        "SO2": request.SO2,
        "CO": request.CO
    }])

    # Debugging: Print the DataFrame columns to verify
    print("Input DataFrame Columns:\n", input_data.columns)

    # Check for missing columns
    expected_columns = [
        'quality_id', 'factor_id', 'pollutant_id', 'Temperature_C',
        'Humidity_%', 'Proximity_to_Industry_km', 'Population_Density',
        'PM2.5', 'PM10', 'NO2', 'SO2', 'CO'
    ]
    for col in expected_columns:
        if col not in input_data.columns:
            raise ValueError(f"Missing column in input data: {col}")

    # Get the prediction from the model
    prediction = model.predict(input_data)

    # Return the prediction
    return {"prediction": prediction[0]}

if __name__ == "main":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Get the PORT from environment
    uvicorn.run(app, host="0.0.0.0", port=port)
