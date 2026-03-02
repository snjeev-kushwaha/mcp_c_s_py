from github.GithubException import GithubException

class GithubToolException(Exception):
    pass

def handle_github_exception(e: GithubException):
    return {
        "error": True,
        "status": e.status,
        "message": e.data.get("message", str(e))
    }