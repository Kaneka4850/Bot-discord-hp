def is_admin(user) -> bool:
    return any(role.permissions.administrator for role in getattr(user, "roles", []))