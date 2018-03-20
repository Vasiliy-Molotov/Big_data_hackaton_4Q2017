import pandas as pd
import xgboost as xgb
def model_from_dict(row_dict):
    df_row = pd.DataFrame(row_dict)
    dm_row = xgb.DMatrix(df_row)
    return bst.predict(dm_row)
model_holder = {'model': model_from_dict}

# Start web server:
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib, time, json
from threading import Thread
try:
    existingServer=myServer
    existingServer.shutdown()
    existingServer.server_close()
except NameError:
    pass  # There's no old server, nothing to do
class ExposeNotebook(BaseHTTPRequestHandler):
    def do_GET(self):
        parameters = urllib.parse.parse_qs(self.path[2:])
        print(parameters)
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"Status": "OK", "Result": model_holder['model'](parameters)}).encode("utf-8"))
myServer = HTTPServer(("", 8081), ExposeNotebook)
Thread(target = myServer.serve_forever).start()