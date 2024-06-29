import logging
from flask import Flask, request, jsonify
import traceback
import io, os
import sys
import time 
import subprocess
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Configure logginga
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to compile and execute code
def execute_code(code):
    # Create a string buffer to capture output
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    # Prepare a dictionary to store the local execution context
    local_vars = {}

    try:
        start_time = time.time()

        # Execute the code within the local_vars context
        exec(code, {}, local_vars)

        end_time = time.time()

        execution_time = end_time - start_time

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Get the captured output
        output = output_buffer.getvalue()

        return {
            'status': 'success',
            'exit_code': 0,
            'output': output,
            'execution_time': execution_time
        }

    except Exception as e:
        # Reset stdout
        sys.stdout = sys.__stdout__

        # Log the exception
        logger.error(f"Error executing code: {e}")
        logger.error(traceback.format_exc())

        # Return the traceback as error
        return {
            'status': 'error',
            'exit_code': 1,  # Indicates error
            'error': str(e),
            'traceback': traceback.format_exc(),
            'execution_time': None
        }


# Function to compile and execute C code without saving to file
def execute_c_code(code):
    c_code = code  # Get C code from request body

    try:
        # Create a temporary directory to store compiled programs
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.c', delete=False)
            temp_file_path = temp_file.name

            # Write the C code to the temporary file
            with open(temp_file_path, 'w') as f:
                f.write(c_code)

            # Compile the C code using gcc
            start_time = time.time()
            compile_process = subprocess.run(['gcc', temp_file_path, '-o', os.path.join(temp_dir, 'temp')], capture_output=True, text=True)

            if compile_process.returncode == 0:
                # Compilation successful, execute the compiled program
                executable_path = os.path.join(temp_dir, 'temp')
                execution_process = subprocess.run([executable_path], capture_output=True)
                output = execution_process.stdout.decode('utf-8')
                end_time = time.time()

                execution_time = end_time - start_time

                # Delete temporary files after execution
                os.remove(temp_file_path)
                os.remove(executable_path)

                return {
                    'status': 'success',
                    'exit_code': 0,
                    'output': output,
                    'execution_time': execution_time
                }
            else:
                # Compilation failed, return error message
                error_message = compile_process.stderr

                # Delete temporary files after compilation failure
                os.remove(temp_file_path)

                return {
                    'status': 'error',
                    'exit_code': 1,  # Indicates error
                    'error': error_message,
                    'execution_time': None
                }
    except Exception as e:
        return {
            'status': 'error',
            'exit_code': 1,  # Indicates error
            'error': str(e),
            'execution_time': None
        }

def check_non_supported_modules(code):
    non_supported_modules = ["import time", "import subprocess"]
    for x in non_supported_modules:
        if x.strip() in code:
            return {
            'status': 'error',
            'exit_code': 1,
            'error': f"{x.replace('import', '').strip()} module is not support in current version of GeekAI compiler",
            'execution_time': None
        }
    return False

def check_supported_langauge(language: str):
    if not language.lower() in ['c', 'c++', 'python', 'java']:
        return {
            'status': 'error',
            'exit_code': 1,
            'error': f"Unsupported language: {language}",
            'execution_time': None
        }
    return False    


# Endpoint to handle POST requests to compile and execute code
@app.route('/compiler', methods=['POST'])
def compile_code():
    print("hi")
    # Get the code from the request body
    data = request.get_json()
    code = data.get('code', '')

    language = data.get('language', 'python').lower()
    
    is_valid_language = check_supported_langauge(language)

    if is_valid_language:
        return jsonify(is_valid_language), 400
    
    if language == 'python':
        non_supported_modules = check_non_supported_modules(code)

        if non_supported_modules:
            return jsonify(non_supported_modules), 400
        
        logger.info(f"Incoming request to compile code: {code}")

        result = execute_code(code)

        logger.info(f"Execution result: {result}")

    elif language == 'c':
        result = execute_c_code(code)

    return jsonify(result)

@app.route("/")
def index():
    return "yes"


if __name__ == '__main__':
    # Run the Flask app using Gunicorn as the server
    app.run(debug=True, port="5001")
