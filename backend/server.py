from flask import Flask, jsonify, json, request, make_response, send_file, Response
from flask_cors import CORS, cross_origin #need to find a way to host both applications on same port, so there is no CORS issues

import pandas as pd 
import numpy as np 
import random
import io

app = Flask(__name__)
cors = CORS(app, support_credentials=True)

@app.route('/api/test-connection')
@cross_origin(supports_credentials=True)
def index():
    # return jsonify({"success": "ok"})
    return {"text": "Python is connected!"}

# this will currently be the endpoint for generating the data and then sending
# out a csv, txt, or excel file with the generated data to the client
# it will probably need to use helper methods along the way...
@app.route('/api/test-send', methods=["POST"])
@cross_origin(supports_credentials=True)
def handleData():
    specific_amt_data = int(json.loads(request.data)['amt'])
    activated_rows = json.loads(request.data)['rows']
    # will loop thru the activated scenarios in the future, but for now, lets just extract the single Scenario being sent
    scenario_details = activated_rows[0][1]

    scenario_file_name = (scenario_details["Scenario"]["fieldValue"]).replace(" ", "_") + "_Test_Data"
    # in the future we will analyze each field, and if its true, we will handle data generation for it... not sure how yet
    # but for now, we will just check for gender and fName + lName
    isGender = scenario_details["Gender"]["fieldValue"]
    isFirstName = scenario_details["firstName"]["fieldValue"]
    isLastName = scenario_details["lastName"]["fieldValue"]

    fields = {
        "Gender": isGender,
        "firstName": isFirstName,
        "lastName": isLastName
    }

    # now we will go on to initialize some dataframe to add our generated data to, and then go on to convert that dataframe and send it out...
    df_columns = [key for key in fields if fields[key]]
    df_indices = [i for i in range(specific_amt_data)]
    scenario_df = pd.DataFrame(index = df_indices, columns=df_columns)

    # go thru cols which were selected
    # initialize an array to hold generate data for the col
    # for n amount of times, where n is user specified, generate data points specific to the col
    # add that list of generated data, of size n to the DF

    # we need to find a way to create a link between data points that are part of the same row
    # we may also have to make sure that the data points are ALL unique... frick
    for column in df_columns:
        generated_col_data = []
        for i in range(specific_amt_data):
            temp_data_hold = generate_col_data(column)
            generated_col_data.append(temp_data_hold)

        scenario_df[column] = generated_col_data

    resp = make_response(scenario_df.to_csv(index=False)) # use flask make_response method, alongside pandas to_csv method
    resp.headers['Access-Control-Allow-Headers'] = 'content-type, content-disposition'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

    resp.headers["Content-Type"] = "text/csv"
    resp.headers["Content-Disposition"] = scenario_file_name

    return resp

@app.route('/api/generate-test-data', methods=["POST"])
@cross_origin(supports_credentials=True)
def generate_test_data():
    #test_field = request.form['fieldName']
    return "Generating Data..."

def generate_col_data(column_name):
    # print(column_name)
    if(column_name == "Gender"):
        return generate_gender()
    if(column_name == "firstName" or column_name == "lastName"):
        return generate_name()
    else:
        return None

# we can have a base function which checks the col we need to generate data for...
# then go on to call a helper method like this to generate tha actual data?
def generate_gender():
    random_chance = random.uniform(0,1)
    if(random_chance <= .5):
        return "M"
    else:
        return "F"

def generate_name():
    random_chance = random.uniform(0,1)
    if(random_chance <= .5):
        return "Tom"
    else:
        return "Bob"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug="True") #need to set host to 0,0,0,0 so it is externally visible... def might need to change in future