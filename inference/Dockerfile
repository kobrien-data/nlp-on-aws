FROM public.ecr.aws/lambda/python:3.10

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_handler.py .

# Command must match: filename.function_name
CMD ["lambda_handler.lambda_handler"]