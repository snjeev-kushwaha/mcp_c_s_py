def tasks_by_assignee_and_status(assignee_email: str, status: str):
    return f'assignee = "{assignee_email}" AND status = "{status}"'

def tasks_by_sprint(sprint_id: int):
    return f'sprint = {sprint_id}'

def tasks_by_assignee(assignee_email: str):
    return f'assignee = "{assignee_email}"'