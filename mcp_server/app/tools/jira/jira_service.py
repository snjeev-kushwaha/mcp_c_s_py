import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from tenacity import retry, stop_after_attempt, wait_exponential
from core.logger import logger
from core.response import success, error
from core.exceptions import MCPException
from tools.jira import jira_queries

load_dotenv()

class JiraService:

    def __init__(self):
        self.base_url = os.getenv("JIRA_BASE_URL")
        self.auth = HTTPBasicAuth(
            os.getenv("JIRA_EMAIL"),
            os.getenv("JIRA_API_TOKEN")
        )
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    # ----------------------------------------
    # Generic Search
    # ----------------------------------------
    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def search_by_jql(self, jql):
        logger.info(f"JQL Search: {jql}")

        url = f"{self.base_url}/rest/api/3/search"
        payload = {"jql": jql}

        response = requests.post(url, json=payload, headers=self.headers, auth=self.auth)

        if response.status_code != 200:
            raise MCPException(response.text, response.status_code)

        return response.json()["issues"]

    # ----------------------------------------
    # Create Ticket
    # ----------------------------------------
    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def create_ticket(self, project_key, summary, description, issue_type="Task"):

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type}
            }
        }

        url = f"{self.base_url}/rest/api/3/issue"
        response = requests.post(url, json=payload, headers=self.headers, auth=self.auth)

        if response.status_code != 201:
            raise MCPException(response.text, response.status_code)

        return response.json()

    # ----------------------------------------
    # Bulk Create
    # ----------------------------------------
    def bulk_create(self, issue_list):
        url = f"{self.base_url}/rest/api/3/issue/bulk"

        payload = {"issueUpdates": issue_list}

        response = requests.post(url, json=payload, headers=self.headers, auth=self.auth)

        if response.status_code != 201:
            raise MCPException(response.text, response.status_code)

        return response.json()

    # ----------------------------------------
    # Assign Ticket
    # ----------------------------------------
    def assign_ticket(self, issue_key, account_id):
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/assignee"
        payload = {"accountId": account_id}

        response = requests.put(url, json=payload, headers=self.headers, auth=self.auth)

        if response.status_code != 204:
            raise MCPException(response.text, response.status_code)

        return {"assigned": True}

    # ----------------------------------------
    # Transition (Move Status)
    # ----------------------------------------
    def transition_issue(self, issue_key, transition_id):
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"

        payload = {"transition": {"id": transition_id}}

        response = requests.post(url, json=payload, headers=self.headers, auth=self.auth)

        if response.status_code != 204:
            raise MCPException(response.text, response.status_code)

        return {"transitioned": True}

    # ----------------------------------------
    # Add Comment
    # ----------------------------------------
    def add_comment(self, issue_key, comment):
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        payload = {"body": comment}

        response = requests.post(url, json=payload, headers=self.headers, auth=self.auth)

        if response.status_code != 201:
            raise MCPException(response.text, response.status_code)

        return response.json()

    # ----------------------------------------
    # Create Subtask
    # ----------------------------------------
    def create_subtask(self, project_key, parent_issue_key, summary):
        payload = {
            "fields": {
                "project": {"key": project_key},
                "parent": {"key": parent_issue_key},
                "summary": summary,
                "issuetype": {"name": "Sub-task"}
            }
        }

        url = f"{self.base_url}/rest/api/3/issue"
        response = requests.post(url, json=payload, headers=self.headers, auth=self.auth)

        if response.status_code != 201:
            raise MCPException(response.text, response.status_code)

        return response.json()

    # ----------------------------------------
    # Get Tasks by Sprint
    # ----------------------------------------
    def get_tasks_by_sprint(self, sprint_id):
        jql = jira_queries.tasks_by_sprint(sprint_id)
        return self.search_by_jql(jql)

    # ----------------------------------------
    # Time Report per Employee
    # ----------------------------------------
    def get_time_report(self, assignee_email):
        jql = jira_queries.tasks_by_assignee(assignee_email)
        issues = self.search_by_jql(jql)

        total_seconds = 0
        for issue in issues:
            total_seconds += issue["fields"].get("timespent") or 0

        return {
            "assignee": assignee_email,
            "total_hours": total_seconds / 3600
        }