import requests
from urllib.parse import urlencode
from wsgiref.simple_server import make_server

url = "http://d3plyik7st1zzz.cloudfront.net/TV9527"

def application(env, start_response):
    path = env['PATH_INFO']
    if path == '/sample.ts':
        start_response('200 OK', [('Content-Type','video/MP2T')])

        r = requests.get(url, stream=True)
        if r.status_code == 200:
            bytes_read = r.raw.read(4096)
            while bytes_read:
                yield bytes_read
                bytes_read = r.raw.read(4096)
        else:
            yield b"Error fetching video stream"
    else:
        start_response('404 Not Found', [])
        yield b'Not Found'

httpd = make_server('', 80, application)
print("Serving on port 80...")

httpd.serve_forever()