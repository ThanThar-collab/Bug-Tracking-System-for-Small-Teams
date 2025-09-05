def user_info(request):
    if request.user.is_authenticated:
        return {
            "username": request.user.username,
            "email": request.user.email,
            "name": request.user.first_name,
            "password": request.user.password,
        }
    return {}