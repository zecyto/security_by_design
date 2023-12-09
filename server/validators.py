import re

class Validator():

    def is_sha256_hash(input):
        sha256_pattern = re.compile(r'^[a-fA-F0-9]{64}$')
        return bool(re.match(sha256_pattern, input))

    def is_email(input):
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return bool(re.match(email_pattern, input))