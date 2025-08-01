from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
import pandas as pd
import uuid
import os
import joblib
import numpy as np

app = FastAPI()

# Load the trained machine learning model
model = joblib.load("../models/model.joblib")

# Directory where all prediction results will be saved
RESULT_DIR = "results"
os.makedirs(RESULT_DIR, exist_ok=True)

# Background function to process a CSV file and write predictions to disk
def run_batch_prediction(file_path: str, job_id: str):
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(file_path)

        # Extract features required by the model
        X = df[["feature1", "feature2", "feature3", "feature4"]]

        # Make predictions
        preds = model.predict(X)

        # Add predictions to the original DataFrame
        df["prediction"] = preds

        # Save the output CSV file with predictions
        output_path = os.path.join(RESULT_DIR, f"{job_id}.csv")
        df.to_csv(output_path, index=False)

    except Exception as e:
        # If something fails, save the error message in a text file
        error_path = os.path.join(RESULT_DIR, f"{job_id}_error.txt")
        with open(error_path, "w") as f:
            f.write(str(e))

# API endpoint to receive a CSV file and trigger batch prediction
@app.post("/predict-batch")
def predict_batch(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    # Accept only CSV files
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    # Generate a unique job ID
    job_id = str(uuid.uuid4())

    # Save the uploaded file to disk temporarily
    input_path = os.path.join(RESULT_DIR, f"{job_id}_input.csv")
    with open(input_path, "wb") as f:
        f.write(file.file.read())

    # Schedule background task for prediction
    background_tasks.add_task(run_batch_prediction, input_path, job_id)

    return {"job_id": job_id, "message": "Prediction started"}

# API endpoint to check the result of a prediction job
@app.get("/result/{job_id}")
def get_result(job_id: str):
    result_path = os.path.join(RESULT_DIR, f"{job_id}.csv")
    error_path = os.path.join(RESULT_DIR, f"{job_id}_error.txt")

    # If the result file exists, return it
    if os.path.exists(result_path):
        return {"status": "done", "result_file": result_path}

    # If an error occurred, return the error details
    elif os.path.exists(error_path):
        with open(error_path, "r") as f:
            error_msg = f.read()
        raise HTTPException(status_code=500, detail=f"Prediction failed: {error_msg}")

    # Otherwise, it's still processing or job_id is invalid
    else:
        return {"status": "pending", "message": "Prediction still running or job_id not found"}



#Usage : 
# curl.exe -X POST "http://127.0.0.1:8000/predict-batch" -F "file=@../data/test_batch.csv"
# curl.exe http://127.0.0.1:8000/result/d18fe308-9f37-41b9-97d2-263d88affdd5    