from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load trained model fromp a previous project
model_path="../models/model.joblib"
model = joblib.load(model_path)

# Define BaseModel for input data

class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float


# Test endpoint
# curl.exe -X GET http://127.0.0.1:8000/

@app.get("/")
def root():
    return {"message": "ML prediction API"}



# Prediction endpoint
# curl.exe -X POST -H "Content-Type: application/json" -d '{\"feature1\":5.1,\"feature2\":3.5,\"feature3\":1.4,\"feature4\":2.2}' http://127.0.0.1:8000/predict
@app.post("/predict")
def predict(data: InputData):
    try:
        X = np.array([[data.feature1, data.feature2, data.feature3, data.feature4]])
        prediction = model.predict(X)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

