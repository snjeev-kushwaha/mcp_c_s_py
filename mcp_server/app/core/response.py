def success(data):
    return {
        "success": True,
        "data": data
    }

def error(message, code=400):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }