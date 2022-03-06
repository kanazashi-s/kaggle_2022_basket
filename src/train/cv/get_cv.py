from . import make_cv1


def get_cv(cv_num: int):
    if cv_num == 1:
        return make_cv1()
