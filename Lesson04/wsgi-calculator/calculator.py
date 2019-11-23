from functools import reduce
import operator

"""
```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```
To submit your homework:
  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!
"""
def html():
    site = '''
    <h1>How to use this site:</h1>
    <p>Use the example below to construct your url</p>
    <ul>
        <li>http://localhost:8080/multiply/3/5  => 15</li>
        <li>http://localhost:8080/add/23/42  => 65</li>
        <li>http://localhost:8080/subtract/23/42  => -19</li>
        <li>http://localhost:8080/divide/22/11 </li>
    </ul>
    '''

    return site


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    total = sum([int(x) for x in args])
    printed_total = f'<h1>Sum: {total}</h1>'

    return printed_total


def subtract(*args):
    args = list(args)
    difference = int(args.pop(0))
    for arg in args:
        difference -= int(arg)

    printed_difference = f'<h1>Difference: {difference}</h1>'

    return printed_difference



def multiply(*args):
    product = 1
    for arg in args:
        product = product * int(arg)

    printed_product = f'<h1>Product: {product}</h1>'

    return printed_product


def divide(*args):
    if "0" in args:
        raise ZeroDivisionError
    args = list(args)
    divide_total = int(args.pop(0))
    for arg in args:
        divide_total = divide_total / int(arg)

    printed_remainder = f'<h1>Divided Total: {divide_total}</h1>'
    return printed_remainder



def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
        '': html,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
    }
    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]

    try:
        path = environ.get("PATH_INFO", None)

        if path is None:
            raise NameError

        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"

    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"

    except ZeroDivisionError:
        status = "200 OK"
        body = "<h1>Cannot divide by zero!</h1>"

    except Exception:
        status = "500 Internal Service Error"
        body ="<h1>Internal Service Error</h1>"

    finally:
        headers.append(("Content-length", str(len(body))))
        start_response(status, headers)
        return [body.encode("utf-8")]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()