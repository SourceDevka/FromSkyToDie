
# def decorator_factory(argument):
#     def decorator(function):
#         def wrapper(*args, **kwargs):
#             funny_stuff()
#             something_with_argument(argument)
#             result = function(*args, **kwargs)
#             more_funny_stuff()
#             return result
#         return wrapper
#     return decorator

class A:
    def __init__(self) -> None:
        self.isBusy = True

    def is_busy_decor(func):
        def wrapper(self, *args, **kwargs):
            while self.isBusy:
                pass

            self.isBusy = True
            res = func(self, *args, **kwargs)
            self.isBusy = False
            return res
        return wrapper
    
    @is_busy_decor
    def p(self):
        print("eeeee")

a = A()
a.p()
  

                