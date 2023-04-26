import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import get_all_entries, get_single_entry, delete_entry, get_entries_by_term, create_entry, update_entry, get_single_mood, get_all_moods

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        '''docstring'''
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "entries":
                if id is not None:
                    response = get_single_entry(id)
                else:
                    response = get_all_entries()
            if resource == "moods":
                if id is not None:
                    response = get_single_mood(id)
                else:
                    response = get_all_moods()
        else:
            (resource, query) = parsed
            print(query)
            if resource == "entries":
                response = get_entries_by_term(query['q'][0])

            # see if the query dictionary has an email key

        self.wfile.write(json.dumps(response).encode())

    def do_DELETE(self):
        '''docstring'''
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "entries":
            delete_entry(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())
    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.

    def do_POST(self):
        '''docstring'''
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new resource
        new_resource = None

        # Add a new resource to the list.
        if resource == "entries":
            new_resource = create_entry(post_body)

        # Encode the new resource and send in response
        self.wfile.write(json.dumps(new_resource).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
