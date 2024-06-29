def check_non_supported_modules(self, code):
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