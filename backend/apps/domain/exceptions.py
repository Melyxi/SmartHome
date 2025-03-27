class ButtonsNotFoundValidationError(Exception):
    status = 422
    message = "Not found some buttons"
