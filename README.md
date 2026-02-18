# Serverless NLP Sentiment Analysis API (AWS)

## 📖 Overview

This project demonstrates end-to-end ML engineering — from training a model locally to deploying it as a live inference API on AWS — without any always-on infrastructure.

The model is built using **TF-IDF feature extraction** and **Logistic Regression** on the [IMDb movie reviews dataset](https://www.kaggle.com/datasets/yasserh/imdb-movie-ratings-sentiment-analysis). Once trained, the model artifacts are stored in **Amazon S3** and served via **AWS Lambda** behind an **Amazon API Gateway** endpoint.

### Why this architecture?

- **Serverless-first** — No EC2 instances or always-on servers; pay only for what you use
- **Production-ready** — REST API with real-time inference
- **Cost-optimized** — Lambda + API Gateway keeps costs near zero at low traffic volumes
- **Observable** — CloudWatch logging for monitoring and debugging
- **Exam-aligned** — Architecture and design decisions map to the [AWS Machine Learning Engineer – Associate (MLA-C01)](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/) exam domains


---

## 🏗️ Architecture

```
User / Client
     │
     ▼
Amazon API Gateway  (HTTP REST endpoint)
     │
     ▼
AWS Lambda          (Model is loaded from S3 on cold start and cached in memory for subsequent invocations.)
     │
     ▼
Amazon S3           (stores trained model artifacts)
     │
Amazon CloudWatch   (logs & monitoring)
```

---

## 📁 Repository Structure

```
nlp-on-aws/
├── data/                   # Sample data and dataset references
├── training/               # Model training scripts and notebooks
├── inference/              # Lambda function handler and dependencies
├── sample-requests/        # Example API request payloads
└── README.md
```

### Folder details

**`data/`** — Contains sample records from the IMDb dataset used for development and testing. The full dataset can be downloaded from [Kaggle](https://www.kaggle.com/datasets/yasserh/imdb-movie-ratings-sentiment-analysis).

**`training/`** — Jupyter notebooks and/or Python scripts for preprocessing text, fitting the TF-IDF vectorizer, training the Logistic Regression classifier, and serialising the model artifacts (`sentiment_pipeline.joblib`) for upload to S3.

**`inference/`** — The AWS Lambda handler (`lambda_function.py`) and any packaging files (e.g. `Dockerfile`, `requirements.txt`). The handler loads the serialized sklearn pipeline (sentiment_pipeline.joblib) from S3 on cold start and performs inference on each invocation.

**`sample-requests/`** — JSON payloads you can use with `curl`, Postman, or the AWS Console to test the deployed endpoint.

---

## 🤖 Model Details

| Property | Value |
|---|---|
| Task | Binary text classification |
| Dataset | IMDb movie reviews |
| Feature extraction | TF-IDF (sklearn `TfidfVectorizer`) |
| Algorithm | Logistic Regression (`sklearn`) |
| Output | `positive` / `negative` label + confidence score |
| Serialisation | `joblib` / `pickle` |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10
- An AWS account with appropriate IAM permissions
- AWS CLI configured locally (`aws configure`)
- The following Python packages (see `training/` for a full requirements file):

```bash
pip install scikit-learn pandas numpy boto3 joblib
```

---

### 1. Prepare the data

Download the full IMDb dataset from Kaggle:

```
https://www.kaggle.com/datasets/yasserh/imdb-movie-ratings-sentiment-analysis
```

Place the CSV in the `data/` directory.

---

### 2. Train the model

Open and run the training notebook in `training/`, or execute the training script directly:

```bash
cd training/
python training.py   # or open the notebook in Jupyter
```

This will produce serialised model artifacts (e.g. `sentiment_pipeline.joblib`).

---

### 3. Upload artifacts to S3

Create an S3 bucket and upload your model files:

```bash
aws s3 mb s3://your-nlp-model-bucket
aws s3 cp sentiment_pipeline.joblib s3://your-nlp-model-bucket/sentiment_pipeline.joblib
```

---

### 4. Deploy the Lambda function

Package and deploy the contents of `inference/` to AWS Lambda. If using the provided `Dockerfile` (container image Lambda):

```bash
cd inference/

aws ecr create-repository \
  --repository-name nlp-sentiment-lambda \
  --region $REGION

# Build the container image
docker build -t nlp-sentiment-lambda .

# Tag and push to Amazon ECR
docker tag nlp-sentiment-lambda:latest \
$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/nlp-sentiment-lambda:latest

aws ecr get-login-password --region $REGION | \
docker login --username AWS --password-stdin \
$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker push \
$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/nlp-sentiment-lambda:latest
```

Then create the Lambda function from the ECR image via the AWS Console or CLI.

Attach an IAM role to the Lambda with at minimum `s3:GetObject` permission on your bucket.

---

### 5. Configure API Gateway

1. In the AWS Console, create a new **HTTP API** in API Gateway
2. Create a `POST` method on a `/predict` resource
3. Set the integration type to **Lambda Function** and point it at your deployed function
4. Deploy the API to a stage (e.g. `prod`)
5. Note your invoke URL — it will look like:
   ```
   https://<api-id>.execute-api.<region>.amazonaws.com/prod/predict
   ```

---

## 🧪 Testing the API

Sample request (see `sample-requests/` for more examples):

```bash
curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/prod/predict \
  -H "Content-Type: application/json" \
  -d '{"review": "This film was an absolute masterpiece. Loved every minute of it!"}'
```

Sample response:

```json
{
  "sentiment": "positive",
  "confidence": 0.97
}
```

---

## 📊 Monitoring

Lambda execution logs are automatically sent to **Amazon CloudWatch Logs**. You can view them in the AWS Console under:

```
CloudWatch > Log groups > /aws/lambda/<your-function-name>
```

Useful metrics to monitor:

- `Invocations` — total number of API calls
- `Errors` — failed invocations
- `Duration` — inference latency (watch for cold starts)
- `Throttles` — if concurrency limits are hit

---

## 💰 Cost Considerations

This architecture is designed to be extremely cost-efficient:

- **Lambda** — first 1M requests/month are free; beyond that, ~$0.20 per 1M requests
- **API Gateway** — first 1M calls/month free under the free tier
- **S3** — negligible for small model artifacts (a few MB)
- **CloudWatch** — 5 GB of log ingestion free per month

At low to moderate traffic, this project can run at effectively **zero ongoing cost**.

---

## 🗺️ AWS MLA-C01 Exam Alignment

This project covers several domains of the AWS Machine Learning Engineer – Associate certification:

| Exam Domain | Covered By |
|---|---|
| Data ingestion & transformation | TF-IDF preprocessing pipeline |
| Model training & evaluation | Logistic Regression with sklearn |
| Model deployment | Lambda + API Gateway |
| ML storage | S3 for model artifacts |
| ML monitoring | CloudWatch Logs & Metrics |
| Cost optimisation | Serverless, pay-per-use architecture |

---

## 📚 References

- [IMDb Dataset on Kaggle](https://www.kaggle.com/datasets/yasserh/imdb-movie-ratings-sentiment-analysis)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Amazon API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [scikit-learn TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [AWS MLA-C01 Exam Guide](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/)

---

## 👤 Author

**kobrien-data** — [GitHub Profile](https://github.com/kobrien-data)

---

## 📄 Licence

This project is open source and available under the [MIT Licence](LICENSE).