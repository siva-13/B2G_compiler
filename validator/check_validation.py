import logging

logger = logging.getLogger(__name__)

class validateRequest:

    def start(self, data):
        code = data.get('code', '')

        is_code_empty = self.check_empty_code_input(code)

        if is_code_empty:
            return is_code_empty
        
        language = data.get('language', 'python').lower()
        
        is_valid_language = self.check_supported_langauge(language)

        if is_valid_language:
            return is_valid_language

        logger.info(f"Incoming request language : {language} and code: {code}")

        if is_valid_language:
            return is_valid_language

    def check_supported_langauge(self, language: str):
        if not language.lower() in ['c', 'c++', 'python', 'java']:
            return {
                'status': 'error',
                'exit_code': 1,
                'error': f"Unsupported language: {language}",
                'execution_time': None
            }
        return False   
    
    def check_empty_code_input(self, code):
        if code == '':
            return {
                        'status': 'success',
                        'exit_code': 0,
                        'output': '',
                        'execution_time': '0.00'
                    }
        return False