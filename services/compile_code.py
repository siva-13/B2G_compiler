import logging
from flask import Flask, request, jsonify
import traceback
import io, os
import sys
import time 
import subprocess
import tempfile

logger = logging.getLogger(__name__)

def execute_python_code(code):
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