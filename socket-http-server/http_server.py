import socket
import sys
import traceback
import mimetypes
import os


def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->
        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """

    # TODO: Implement response_ok
    return b"\r\n".join([
        b'HTTP/1.1 200 OK',
        bytes(f'Content-Type: {mimetype}', 'utf-8'),
        b'',
        body,
    ])


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""

    # TODO: Implement response_method_not_allowed
    return b"\r\n".join([
        b'HTTP/1.1 405 Method not Allowed',
        b'',
        b"You can't do that on this server"
    ])


def response_not_found():
    """Returns a 404 Not Found response"""

    # TODO: Implement response_not_found
    return b'\r\n'.join([
        b'HTTP/1.1 404 Page not found',
        b'',
        b'The page you are looking for is in another castle'
    ])


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.
    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    # TODO: implement parse_request
    method, path, version = request.split('\r\n')[0].split(" ")

    if method != 'GET':
        raise NotImplementedError

    return path


def response_path(path):
    """
    This method should return appropriate content and a mime type.
    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.
    If the path is a file, it should return the contents of that file
    and its correct mimetype.
    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.
    Ex:
        response_path('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")
        response_path('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")
        response_path('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")
        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError
    """
    # relative_path = os.path.join('webroot', path.strip('/'))
    relative_path = os.path.join('webroot', *path.strip('/').split('/'))

    if not os.path.lexists(relative_path):
        raise NameError
    elif os.path.isdir(relative_path):
        mime_type = 'text/plain'
        content = '\n'.join(os.listdir(relative_path))
        content = bytes(content, 'utf-8')
    else:
        mime_type = mimetypes.guess_type(relative_path)[0]
        with open(relative_path, 'rb') as file:
            content = file.read()

    # TODO: Raise a NameError if the requested content is not present
    # under webroot.

    # TODO: Fill in the appropriate content and mime_type give the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py

    # If the path is "make_time.py", then you may OPTIONALLY return the
    # result of executing `make_time.py`. But you need only return the
    # CONTENTS of `make_time.py`.

    # content = b"not implemented"
    # mime_type = b"not implemented"

    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 11000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(10)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break

                    if not request:
                        raise Exception("")

                print("Request received:\n{}\n\n".format(request))
                # TODO: Use parse_request to retrieve the path from the request.
                try:
                    path = parse_request(request)
                    # TODO: Use response_path to retrieve the content and the mimetype,
                    # based on the request path.
                    content, mime_type = response_path(path)
                    # TODO; If parse_request raised a NotImplementedError, then let
                    # response be a method_not_allowed response. If response_path raised
                    # a NameError, then let response be a not_found response. Else,
                    # use the content and mimetype from response_path to build a
                    # response_ok.
                    response = response_ok(
                        body=content,
                        mimetype=mime_type
                    )
                except NotImplementedError:
                    response = response_method_not_allowed()
                except NameError:
                    response = response_not_found()

                conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)
