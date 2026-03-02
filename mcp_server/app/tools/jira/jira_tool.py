from core.auth import require_role
from core.response import success, error
from tools.jira.jira_service import JiraService

jira_service = JiraService()

# ------------------------------
# Create Ticket
# ------------------------------
def create_ticket_tool(args, user):
    try:
        result = jira_service.create_ticket(
            args["project_key"],
            args["summary"],
            args["description"],
            args.get("issue_type", "Task")
        )
        return success(result)
    except Exception as e:
        return error(str(e))


# ------------------------------
# Bulk Create (Admin only)
# ------------------------------
def bulk_create_tool(args, user):
    try:
        require_role(user["role"], ["admin"])
        result = jira_service.bulk_create(args["issues"])
        return success(result)
    except Exception as e:
        return error(str(e))


# ------------------------------
# Transition Issue
# ------------------------------
def transition_issue_tool(args, user):
    try:
        require_role(user["role"], ["dev", "manager"])
        result = jira_service.transition_issue(
            args["issue_key"],
            args["transition_id"]
        )
        return success(result)
    except Exception as e:
        return error(str(e))


# ------------------------------
# Time Report (Manager only)
# ------------------------------
def time_report_tool(args, user):
    try:
        require_role(user["role"], ["manager"])
        result = jira_service.get_time_report(args["assignee_email"])
        return success(result)
    except Exception as e:
        return error(str(e))