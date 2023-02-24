from http.server import HTTPServer, BaseHTTPRequestHandler
import requests


class ProxyServer(BaseHTTPRequestHandler):

    def _set_response(self, status_code=200, content=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):

        response = requests.get(url='https://news.ycombinator.com/'+self.path[1:])
        html = None
        content = response.content

        try:
            if content.decode()[0] == '<':
                words = self.edit(text=response.content.decode())
                for word, edited_word in words.items():
                    content = content.replace(word.encode('UTF-8'), edited_word.encode('UTF-8'))

        except UnicodeDecodeError:
            pass

        self._set_response(status_code=200, content=content)

    @staticmethod
    def edit(text):

        import re
        text = re.sub(r'<[^>]*>', '', text)
        words = re.findall(pattern=r'\b[a-zA-Z]{6}\b[\s,!?\.]', string=text)

        dictionary = {}
        for word in words:
            dictionary[word] = word[:-1]+'&#8482;'+word[-1]
        return dictionary


def run(server_class=HTTPServer, handler_class=ProxyServer, host='localhost', port=8000):

    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    run()
