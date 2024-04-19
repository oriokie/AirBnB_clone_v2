#!/usr/bin/python3
"""
Write a script that starts a Flask web application:
    Your web application must be listening on 0.0.0.0, port 5000
    Routes:
        - /: display “Hello HBNB!”
        - /hbnb: display “HBNB”
        - /c/<text>: display “C ”, followed by the value of the text variable
          (replace underscore _ symbols with a space )
        - /python/(<text>): display “Python ”, followed by the value of the
          text variable (replace underscore _ symbols with a space )
            - The default value of text is “is cool”
        - /number/<n>: display “n is a number” only if n is an integer
        - /number_template/<n>: display a HTML page only if n is an integer:
            - h1 tag: “Number: n” inside the tag body
    You must use the option strict_slashes=False in your route definition
"""

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_HBNB():
    """ Display hello HBNB """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Display HBNB """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_something(text):
    """ Display C """
    new_text = text.replace('_', ' ')
    return 'C {}'.format(new_text)


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """ Display Python """
    if '_' in text:
        text = text.replace('_', ' ')
    return 'Python {}'.format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ Display if n is a number """
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def html_number(n):
    """ Display if n is a number in html """
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
