from flask import session, redirect
# functools contains several helper functions that we can use to change other functions, wraps() function is a decorator itself
from functools import wraps

# redirect user who isn't logged in or to run the original route function for a user who is logged in

# call function that expects to receive another function as an argument (which it captures as the func parameter)
def login_required(func):
    # preserves the original function's name when creating the wrapped function
    @wraps(func)
    # *args and **kwargs ensure that no matter how many arguments are given (if any) the wrapped_function() captures them all, so we preserve any arguments the original function received
    def wrapped_function(*args, **kwargs):
        # if logged in, call original function with original arguments
        if session.get('loggedIn') == True:
            return func(*args, **kwargs)
        
        return redirect('/login')

    return wrapped_function