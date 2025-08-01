import pandas as pd
import json
import requests

API_URL = "http://127.0.0.1:8000/predict"

def predict_from_csv(csv_path: str, output_csv: str = "predictions.csv"):
    df = pd.read_csv(csv_path)
    predictions = []

    for i, row in df.iterrows():
        payload = {
            "feature1": row["feature1"],
            "feature2": row["feature2"],
            "feature3": row["feature3"],
            "feature4": row["feature4"]
        }
        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()
            predictions.append(result.get("prediction", None))
        except Exception as e:
            predictions.append(f"error: {e}")

    df["prediction"] = predictions
    df.to_csv(output_csv, index=False)
    print(f"Predictions written to {output_csv}")


def predict_from_json(json_path: str, output_csv: str = "predictions.csv"):
    with open(json_path, "r") as f:
        data = json.load(f)

    inputs = []
    predictions = []

    for i, payload in enumerate(data):
        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()
            inputs.append(payload)
            predictions.append(result.get("prediction", None))
        except Exception as e:
            inputs.append(payload)
            predictions.append(f"error: {e}")

    df = pd.DataFrame(inputs)
    df["prediction"] = predictions
    df.to_csv(output_csv, index=False)
    print(f"Predictions written to {output_csv}")


# predict_from_csv("./data/input.csv",output_csv="./data/csv_results.csv")
predict_from_json("./data/input.json",output_csv="./data/json_results.csv")
