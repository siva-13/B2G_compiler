import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from validator.check_validation import validateRequest
from services.compile_code import execute_c_code, execute_python_code
from utils import check_non_supported_modules

app = Flask(__name__)
CORS(app)

# Configure logginga
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Endpoint to handle POST requests to compile and execute code
@app.route('/compiler', methods=['POST'])
def compile_code():
    # Get the code from the request body
    data = request.get_json()

    validate_request = validateRequest().start(data)

    if validate_request:
        return jsonify(validate_request)
    
    language = data.get('language').lower()
    code  = data.get('code')

    if language == 'python':
        non_supported_modules = check_non_supported_modules(code)

        if non_supported_modules:
            return jsonify(non_supported_modules), 400

        result = execute_python_code(code)

        logger.info(f"Execution result: {result}")

    elif language == 'c':

        result = execute_c_code(code)

        logger.info(f"Execution result: {result}")

    return jsonify(result)

@app.route("/")
def index():
    return "working"

if __name__ == '__main__':
    # Run the Flask app using Gunicorn as the server
    app.run(debug=True, port="5001")
