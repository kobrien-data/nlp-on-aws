import os
import joblib
import boto3
import json

BUCKET_NAME = "mla-c01-sentiment-model"
MODEL_KEY = "sentiment_pipeline.joblib"
LOCAL_MODEL_PATH = "/tmp/sentiment_pipeline.joblib"

s3 = boto3.client("s3")

model = None

def load_model(force_reload=False):
    global model
    # Delete old file if forcing reload
    if force_reload and os.path.exists(LOCAL_MODEL_PATH):
        os.remove(LOCAL_MODEL_PATH)
        model = None

    if model is None:
        print("Downloading model from S3...")
        s3.download_file(BUCKET_NAME, MODEL_KEY, LOCAL_MODEL_PATH)
        print("Loading model from:", LOCAL_MODEL_PATH)
        model = joblib.load(LOCAL_MODEL_PATH)
        print("Model loaded successfully:", type(model))
    return model

def lambda_handler(event, context):
    try:
        # Force reload so we are guaranteed to use the new model
        model = load_model(force_reload=True)

        body = json.loads(event.get("body", "{}"))
        review = body.get("review")

        if not review:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing 'review' field"})}

        prediction = model.predict([review])[0]
        probability = model.predict_proba([review])[0]
        sentiment = "positive" if prediction == 1 else "negative"
        confidence = float(max(probability))

        return {
            "statusCode": 200,
            "body": json.dumps({"sentiment": sentiment, "confidence": confidence})
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
