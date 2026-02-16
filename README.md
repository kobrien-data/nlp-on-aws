# Serverless NLP Sentiment Analysis API (AWS)

## Overview

This project demonstrates how to design, train, and deploy a machine learning model using a cost-efficient, serverless AWS architecture.

The goal of the project is to build a binary sentiment classifier that predicts whether a movie review is **positive or negative**, and expose the model as a production-style REST API.

The model is trained locally using TF-IDF feature extraction and Logistic Regression on the IMDb movie reviews dataset. The trained artifacts are then deployed to AWS using:

- AWS Lambda for inference
- Amazon API Gateway for HTTP access
- Amazon S3 for model storage
- Amazon CloudWatch for logging and monitoring

This project was intentionally designed to:
- Demonstrate practical ML engineering skills
- Follow serverless and cost-optimized cloud design principles
- Align with AWS Machine Learning Engineer – Associate (MLA-C01) exam domains
- Avoid always-on infrastructure

The final result is a lightweight, production-ready inference API that can classify text in real time while maintaining minimal AWS costs.

Data source: https://www.kaggle.com/datasets/yasserh/imdb-movie-ratings-sentiment-analysis