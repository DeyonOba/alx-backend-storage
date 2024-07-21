#!/usr/bin/python3
from functools import wraps
import logging
import time
"""
Learn and practice basic concepts about Python decorator.
"""

def function_1():
    print("Why Python?")

print("Exercise 1: Understand Python first class function")

"""
Python first class function allows us to treat function as any other object,
we can return function, and assign function to variables.
"""

func = function_1
print(func())

def function_2(func):
    print(func())
    
def outer_function(msg):
    def inner_function(comment):
        print(msg)
        print("", comment, sep="\n")
    return inner_function

func_1 = outer_function("What would this function print?, what's your answer?")
print(func_1("I don't know let's find out"))

def function_decorator(function):
    def function_wrapper(*args, **kwargs):
        print("What would this function print?, what's your answer?")
        return function(*args, **kwargs)
    return function_wrapper

@function_decorator
def display(answer):
    print("Calling display now")
    print(answer)

display("I don't know!")


logging.basicConfig(filename=__name__+".log", level=logging.INFO)
"""
def log_function(function):
    def wrapper(*args, **kwargs):
        logging.info("{} function with arguments {}".format(function.__name__, args))
        return function(*args, **kwargs)
    return wrapper

def timer(function):
    def wrapper(*args, **kwargs):
        now = time.perf_counter()
        func = function(*args, **kwargs)
        time_elapsed = time.perf_counter() - now
        print("Time taken to run function {} is {} seconds".format(function.__name__, time_elapsed))
        return func
    return wrapper

@log_function
@timer
def add(x, y):
    print(f"{x=} {y=} -> {x} + {y} = {x + y}")
"""
# Comment below explains the drawback of the code above
"""
The code above work well in capturing the time of execution of the function `add`, and logs the function name and the arguments passed.
But the code above has one drawback, it does not accurately capture the correct function name been executed, rather than logging in
`add` with the relative arguments passed it logs in `wrapper`, this is because the function integrity is not maintained after the function
is passed into the two decorators, to solve this problem I'd use the functool wraps from Python.
"""
def log_function(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        logging.info("{} function with arguments {}".format(function.__name__, args))
        return function(*args, **kwargs)
    return wrapper

def timer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        now = time.perf_counter()
        func = function(*args, **kwargs)
        time_elapsed = time.perf_counter() - now
        print("Time taken to run function {} is {} seconds".format(function.__name__, time_elapsed))
        return func
    return wrapper

@log_function
@timer
def add(x, y):
    print(f"{x=} {y=} -> {x} + {y} = {x + y}")    
add(2, 3)