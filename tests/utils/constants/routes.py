from enum import Enum


class APIRoutes(str, Enum):
    login_page = "/v1/login"
    auth = "/protected"
    create_new_user = "/user/"
    count = "/user/count"
    total = "/user/total"
    user_all = "/user/all"
    projects = "/user/project"
    inactive = "/user/inactive"
    user_credentials = "/user/user-credentials"
    projects_all = "/user/projects"
    register = "/user/register/range"
    user_by_month = "/user/registered-in-month/"
    zero_login = "/user/login/zero-login"
    success_login = "/user/login/success"
    fail_login = "/user/login/fail"

    def __str__(self) -> str:
        return self.value
