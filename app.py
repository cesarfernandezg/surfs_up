from flask import Flask

# create a Flask instance
app = Flask(__name__) # Variables with underscores before and after them are called magic methods in Python.

# create Flask routes
@app.route('/')
# This denotes that we want to put our data at the root of our routes. 
# The forward slash is commonly known as the highest level of hierarchy in any computer system.
def hello_world():
    return "Hello World"






