from flask import Flask, jsonify
import sys 
sys.path.insert(0, './algorithm/bimaru.py')
from bimaru import get_steps
from flask_cors import CORS

app = Flask(__name__)


CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/", methods=["GET"])
def hello_world():
    info = []
    steps = get_steps()
    for step in steps:
        step_list = []
        for i in range(10):
            for j in range(10):
                step_list.append(step[i][j])
        info.append(step_list)
    return jsonify(info)