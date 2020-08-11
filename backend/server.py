from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Python is connected!"

@app.route('/generate-test-data', methods=['POST'])
def generate_test_data():
    #test_field = request.form['fieldName']
    return "Generating Data..."

if __name__ == '__main__':
    app.run(debug=True)