from flask import *
import json,time

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home_page():
    data_set = {'Page':'Home','Message':'Welcome to Homepage','Timestamp':time.strftime('%H:%M:%S')}
    json_dump = json.dumps(data_set)
    return json_dump


if __name__ == '__main__':
    app.run(port=7777)