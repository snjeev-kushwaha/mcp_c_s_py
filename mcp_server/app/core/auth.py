def require_role(user_role, allowed_roles):
    if user_role not in allowed_roles:
        raise Exception("Unauthorized: insufficient permissions")