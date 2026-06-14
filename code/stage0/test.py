def before_run(func):
    def wrapper(*args, **kwargs):
        print("函数马上开始")
        result = func(*args, **kwargs)
        return result
    return wrapper

def after_run(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("函数已经结束")
        return result
    return wrapper

@before_run
@after_run
def say(name):
    print(f"Hello, {name}")

say("Alice")