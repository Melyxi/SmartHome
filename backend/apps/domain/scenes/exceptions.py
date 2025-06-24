
class SceneNotFoundError(Exception):
    status = 404
    message = "Not found Scene"

class FileSyntaxError(Exception):
    status = 400
    message = "File syntax error!"