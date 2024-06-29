import requests
import concurrent.futures

# Function to send POST request to the Flask endpoint
def send_request(code):
    url = 'http://51.20.123.126/compiler'  # Replace with your Flask endpoint URL
    headers = {'Content-Type': 'text/json'}
    
    try:
        response = requests.post(url, headers=headers, json={"code":code})
        response.raise_for_status()  # Raise exception for bad status codes

        # Check if response is valid JSON
        try:
            return response.json()
        except ValueError as e:
            return {'error': f'Invalid JSON response: {str(e)}'}
    
    except requests.exceptions.RequestException as e:
        return {'error': f'Request failed: {str(e)}'}

# Example C code to compile and execute
code_to_compile = """
#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}
"""

# Number of concurrent requests to send
num_requests = 5

# List to store future objects
futures = []

# Send multiple requests concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    for _ in range(num_requests):
        future = executor.submit(send_request, code_to_compile)
        futures.append(future)

# Collect results from futures
results = [future.result() for future in futures]

# Print results
for result in results:
    print(result)
