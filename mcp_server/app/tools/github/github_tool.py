from tools.github.github_service import GithubService

github_service = GithubService()

def create_github_repo_tool(args: dict):
    return github_service.create_repo(
        name=args["name"],
        description=args.get("description", ""),
        private=args.get("private", False)
    )

def get_all_github_repos_tool(args: dict):
    return github_service.get_all_repos()


GITHUB_TOOLS = [
    {
        "name": "create_github_repo",
        "description": "Create a new GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "private": {"type": "boolean"}
            },
            "required": ["name"]
        },
        "handler": create_github_repo_tool
    },
    {
        "name": "get_all_github_repos",
        "description": "Get all GitHub repositories of the authenticated user",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "handler": get_all_github_repos_tool
    }
]