def is_manager(user):
    return user.is_authenticated and user.groups.filter(name="Managers").exists()