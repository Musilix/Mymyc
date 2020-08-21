from flask import Flask, jsonify, json, request
from flask_cors import CORS, cross_origin #need to find a way to host both applications on same port, so there is no CORS issues

app = Flask(__name__)
cors = CORS(app, support_credentials=True)

@app.route('/api/test-connection')
@cross_origin(supports_credentials=True)
def index():
    # return jsonify({"success": "ok"})
    return {"text": "Python is connected!"}

@app.route('/api/test-send', methods=["POST"])
@cross_origin(supports_credentials=True)
def handleData():
    activated_rows = json.loads(request.data)['rows']
    print(activated_rows)

    return jsonify(activated_rows)

@app.route('/api/generate-test-data', methods=["POST"])
@cross_origin(supports_credentials=True)
def generate_test_data():
    #test_field = request.form['fieldName']
    return "Generating Data..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug="True") #need to set host to 0,0,0,0 so it is externally visible... def might need to change in future