# pylint: disable=missing-module-docstring,missing-function-docstring,line-too-long

def static_vars(**kwargs):
    def decorate(func):
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func

    return decorate
