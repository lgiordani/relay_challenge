# This is the entrypoint for AWS lambda

from apig_wsgi import make_lambda_handler
from wsgi import app

# Configure this as your entry point in AWS Lambda
lambda_handler = make_lambda_handler(app)
