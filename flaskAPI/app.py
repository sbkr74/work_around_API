from flask import Flask,request,jsonify
import json,time

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home_page():
    data_set = {'Page':'Home','Message':'Welcome to Homepage','Timestamp':time.strftime('%H:%M:%S')}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/user/',methods=['GET'])
def request_page():
    user_query = str(request.args.get('user'))          #   /user/?=user=USERNAME
    data_req = {'Page':'Request','Message':f'Successfull got request query from {user_query}','Timestamp':time.strftime('%H:%M:%S')}
    return jsonify(data_req)

@app.route('/data',methods=['GET'])
def show_data():
    filepath = 'flaskAPI/story/files/stories_data.json'
    try:
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "Stories data not found."})
    

if __name__ == '__main__':
    app.run(port=7777)