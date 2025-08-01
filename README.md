# FastAPI Training Repository

This repository contains various projects developed to train and improve skills with FastAPI.

### Basic App

A simple application to understand how FastAPI works, including handling requests and basic functionality.

### ML_API

A training project focused on building prediction APIs with FastAPI, including command-line usage, dedicated Python scripts, input file handling, and output generation. The goal is to learn deployment and automate predictions.

### async_batch_predict_api

An advanced project implementing an asynchronous batch prediction system. Users can upload a CSV file containing multiple input rows, and the API processes the predictions in the background. A unique job ID is returned, which can be used to retrieve the results once the predictions are completed.

Key features:
- Asynchronous background task execution using `BackgroundTasks`
- Job tracking via unique `job_id`
- Error handling and logging for failed jobs
- CSV file support for both input and output
- Clear separation between upload and result access endpoints

Endpoints:
- `POST /predict-batch`: Upload a CSV file to start a prediction job
- `GET /result/{job_id}`: Retrieve the result file or error status for a given job

The goal of this project is to simulate realistic batch inference pipelines and demonstrate how to handle background processing, state tracking, and file management using FastAPI.
