
class DatabaseValidateError(Exception):
    def __init__(self, error_message, status, code, orig):
        self.orig = orig
        self.error_message = error_message
        self.status = status
        self.code = code

        self.field = None
        self.value = None
        self.pretty_message = ""

        self.parse_error_message()

        self.create_pretty_message()

    def parse_error_message(self):
        detail_message = self.error_message.split("DETAIL:")[-1]
        self.field = detail_message.split(')=')[0].split('(')[-1]
        self.value = detail_message.split('=(')[1].split(')')[0]


    def create_pretty_message(self):
        pass

class UniqueViolationValidateError(DatabaseValidateError):
    def create_pretty_message(self):
        self.pretty_message = {self.field: f"'{self.value}' is already exist!"}
