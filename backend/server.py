from flask import Flask, jsonify, json, request, make_response, send_file, Response
from flask_cors import CORS, cross_origin #need to find a way to host both applications on same port, so there is no CORS issues

import io
import pandas as pd 
import numpy as np 
import random
from io import BytesIO
import zipfile

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

    # for possible zipping - may improve process in future... it's only me tho, so no outside perspective
    zipThatBitch = (len(activated_rows) > 1)
    filesToSend = []

    for activated_row in activated_rows:
        data_to_send = generate_data(activated_row, specific_amt_data)
        filesToSend.append(data_to_send)
        
    # print(filesToSend)
    return send_data(filesToSend, zipThatBitch)

def generate_data(activated_row, amt):
    df_values = extract_data(activated_row)
    # print("DATAFRAME VALS: ", df_values["fields"], "\n")
    scenario_df = construct_dataframe(df_values, amt)

    return {"scenario_df": scenario_df, "df_values": df_values}
    # convert to specified file type?
    # return send_data(scenario_df, df_values)

def extract_data(activated_row):
    # will loop thru the activated scenarios in the future, but for now, lets just extract the single Scenario being sent
    scenario_details = activated_row[1]

    # print(scenario_details)
    # print("\n")

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
        # might need to add more for each field -- this will hold if the curr scenario has the field marked as true... probably a better way to do this
    }

    # these will always be the vals we need for constructing a df for a scenario... the scenarios details, the file name we want, and the fields tru/false vals of the scenarios' 
    return {"details": scenario_details, "file_name": scenario_file_name, "fields": fields}

def construct_dataframe(df_values, amt):
    
    # now we will go on to initialize some dataframe to add our generated data to, and then go on to convert that dataframe and send it out...
    df_columns = [key for key in df_values["fields"] if df_values["fields"][key]]
    df_indices = [i for i in range(amt)]
    scenario_df = pd.DataFrame(index = df_indices, columns = df_columns)

    # go thru cols which were selected
    # initialize an array to hold generate data for the col
    # for n amount of times, where n is user specified, generate data points specific to the col
    # add that list of generated data, of size n to the DF

    # we need to find a way to create a link between data points that are part of the same row
    # we may also have to make sure that the data points are ALL unique... frick
    for column in df_columns:
        generated_col_data = []
        for i in range(amt):
            temp_data_hold = generate_col_data(column)
            generated_col_data.append(temp_data_hold)

        scenario_df[column] = generated_col_data

    return scenario_df

def send_data(filesToSend, zipThatBitch):
    resp = None

    if(zipThatBitch):
        memory_file = BytesIO()

        with zipfile.ZipFile(memory_file, 'w') as zf:
            for file in filesToSend:
                # print(file["scenario_df"])
                # print("theres a file")
                # might need to change this discrete addition of ".csv" conditionally to excel or txt according to what the user specifies
                data = zipfile.ZipInfo(file["df_values"]["file_name"] + ".csv")
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, file["scenario_df"].to_csv(None, encoding='utf-8', index=False))

        memory_file.seek(0)
        resp = send_file(memory_file, mimetype="application/zip", as_attachment=True, attachment_filename="Scenarios.zip")
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Allow-Headers'] = "type-stream"
        resp.headers['Access-Control-Expose-Headers'] = 'Type-Stream'
        resp.headers["Type-Stream"] = "zip"

        # resp = {"Message": "Good to go!"}
    # if there is one file, zipTHatBitch should be false, so no need to do zipping of files...
    else:
        # create resp with the df that was generated, set necessary headers to send the file name we want to use, and content type
        resp = make_response(filesToSend[0]["scenario_df"].to_csv(index=False)) # use flask make_response method, alongside pandas to_csv method
        resp.headers['Access-Control-Allow-Headers'] = 'content-type, content-disposition'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        resp.headers["Content-Type"] = "text/csv"

        resp.headers["Content-Disposition"] = filesToSend[0]["df_values"]["file_name"]

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