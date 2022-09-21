def site_title(request):
        return {
            'site_title':"Hotel Zero",
        }

def get_roles(request):
    role = str(request.user.groups.all()[0])
    return {
            'role':role
        }