import os
from github import Github
from github.GithubException import GithubException
from dotenv import load_dotenv
from app.config import config
from .github_exceptions import handle_github_exception

load_dotenv()

class GithubService:
    def __init__(self):
        token = config.GITHUB_TOKEN
        if not token:
            raise Exception("GITHUB_TOKEN not found")

        self.client = Github(token)
        self.user = self.client.get_user()

    # -----------------------
    # Create User Repo
    # -----------------------
    def create_repo(self, name: str, description: str = "", private: bool = False):
        try:
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private
            )

            return {
                "name": repo.name,
                "url": repo.html_url,
                "private": repo.private
            }
        except GithubException as e:
            return handle_github_exception(e)

    # -----------------------
    # Get All Repos
    # -----------------------
    def get_all_repos(self):
        try:
            repos = self.user.get_repos()

            return [
                {
                    "name": repo.name,
                    "url": repo.html_url,
                    "private": repo.private
                }
                for repo in repos
            ]
        except GithubException as e:
            return handle_github_exception(e)

    # -----------------------
    # Org Repo Creation
    # -----------------------
    def create_org_repo(self, org_name, name, description="", private=True):
        try:
            org = self.client.get_organization(org_name)

            repo = org.create_repo(
                name=name,
                description=description,
                private=private
            )

            return {
                "name": repo.name,
                "url": repo.html_url
            }
        except GithubException as e:
            return handle_github_exception(e)

    # -----------------------
    # Branch Creation
    # -----------------------
    def create_branch(self, repo_name, new_branch, base_branch="main"):
        try:
            repo = self.user.get_repo(repo_name)

            base_ref = repo.get_git_ref(f"heads/{base_branch}")

            repo.create_git_ref(
                ref=f"refs/heads/{new_branch}",
                sha=base_ref.object.sha
            )

            return {"branch": new_branch}
        except GithubException as e:
            return handle_github_exception(e)

    # -----------------------
    # Create File
    # -----------------------
    def create_file(self, repo_name, file_path, content, commit_message="Add file"):
        try:
            repo = self.user.get_repo(repo_name)

            repo.create_file(
                path=file_path,
                message=commit_message,
                content=content,
                branch="main"
            )

            return {"file": file_path}
        except GithubException as e:
            return handle_github_exception(e)

    # -----------------------
    # Update File
    # -----------------------
    def update_file(self, repo_name, file_path, content, commit_message="Update file"):
        try:
            repo = self.user.get_repo(repo_name)
            file = repo.get_contents(file_path)

            repo.update_file(
                path=file.path,
                message=commit_message,
                content=content,
                sha=file.sha
            )

            return {"file": file_path}
        except GithubException as e:
            return handle_github_exception(e)