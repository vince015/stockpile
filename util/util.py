
def is_crew(user):
    return user.is_superuser or user.groups.filter(name='Crew').exists()

def is_cashier(user):
    return user.is_superuser or user.groups.filter(name='Cashier').exists()