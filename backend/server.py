from flask import Flask, jsonify, json, request, make_response, send_file, Response
from flask_cors import CORS, cross_origin #need to find a way to host both applications on same port, so there is no CORS issues
from io import BytesIO

import pandas as pd 
import numpy as np 

import random, datetime, zipfile, io, requests, string

app = Flask(__name__)
cors = CORS(app, support_credentials=True)

# url to try and identify gender from fname field...
url = "https://genderify3.p.rapidapi.com/genderify"
headers = {
    'x-rapidapi-host': "genderify3.p.rapidapi.com",
    'x-rapidapi-key': "d5b949385cmsh5270cc327f01e01p19ecb0jsnfc22637bb9df"
}

# querystring = {"text": "Kareem"}
# gender = requests.request("GET", url, headers=headers, params=querystring)
# print(gende)r

# for generating names when email is chosen, but fName and lName are not...
letters = string.ascii_lowercase

# not really sure if I should make these global, but I dont want to initialize these vals each time i have
# to generate a new name... good to just have a static reference... maybe not the best idea to put it here tho idk
fname_data_src = "./static_mapping_data/first_names.csv"
fname_csv = pd.read_csv(fname_data_src)
# for some reason, even tho i set the header to first_name, i must reference it with firstname instead... weird
fname_size = fname_csv["firstname"].size #why not use len()? idk... lets just leave it for now

# either make a csv for lnames or combine the two and edit var names

# need data source for city state county mappings
location_data_src = "./static_mapping_data/states_to_cities_to_counties.csv"
location_data_csv = pd.read_csv(location_data_src)
# keep global ref to size of this location csv
location_data_size = len(location_data_csv) - 1

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
    # print(df_values)
    # print("DATAFRAME VALS: ", df_values["fields"], "\n")
    scenario_df = construct_dataframe(df_values, amt)

    return {"scenario_df": scenario_df, "df_values": df_values}
    # convert to specified file type?
    # return send_data(scenario_df, df_values)

def extract_data(activated_row):
    # will loop thru the activated scenarios in the future, but for now, lets just extract the single Scenario being sent
    scenario_details = activated_row[1]
    scenario_file_name = (scenario_details["Scenario"]["fieldValue"]).replace(" ", "_") + "_Test_Data"

    # in the future we will analyze each field, and if its true, we will handle data generation for it... not sure how yet
    # but for now, we will just check for gender and fName + lName

    # maybe create a mapping in near future
    isGender = scenario_details["Gender"]["fieldValue"]
    isAddress = scenario_details["Address"]["fieldValue"]
    isDOB = scenario_details["DOB"]["fieldValue"]
    isSpouseFirstName = scenario_details["Spouse_First_Name"]["fieldValue"]
    isSpouseLastName = scenario_details["Spouse_Last_Name"]["fieldValue"]
    isSpouseDOB = scenario_details["Spouse_DOB"]["fieldValue"] 
    isStreetAddress = scenario_details["Street_Address"]["fieldValue"] 
    isApt = scenario_details["Apt"]["fieldValue"] 
    isCity = scenario_details["City"]["fieldValue"] 
    isCounty = scenario_details["County"]["fieldValue"] 
    isZip = scenario_details["Zip"]["fieldValue"] 
    isState = scenario_details["State"]["fieldValue"] 
    isRentOrOwn = scenario_details["Rent_or_Own"]["fieldValue"]
    isEmailAddress = scenario_details["Email_Address"]["fieldValue"] 
    isDateOfPurchase = scenario_details["Date_of_Purchase"]["fieldValue"] 
    isMake = scenario_details["Make"]["fieldValue"] 
    isModel = scenario_details["Model"]["fieldValue"] 
    isFinance = scenario_details["Finance"]["fieldValue"]
    isFirstName = scenario_details["firstName"]["fieldValue"]
    isLastName = scenario_details["lastName"]["fieldValue"]
    isPrimary_Phone = scenario_details["Primary_Phone"]["fieldValue"]
    isSecondary_Phone = scenario_details["Secondary_Phone"]["fieldValue"]


    fields = {
        "firstName": isFirstName,
        "lastName": isLastName,
        "Spouse_First_Name": isSpouseFirstName,
        "Spouse_Last_Name": isSpouseLastName,
        "Gender": isGender,
        "DOB": isDOB,
        "Spouse_DOB": isSpouseDOB,
        "State": isState,
        "City": isCity,
        "County": isCounty,
        "Zip": isZip,
        "Address": isAddress,
        "Street_Address": isStreetAddress,
        "Apt": isApt,
        "Rent_or_Own": isRentOrOwn,
        "Email_Address": isEmailAddress,
        "Primary_Phone": isPrimary_Phone,
        "Secondary_Phone": isSecondary_Phone,
        "Date_of_Purchase": isDateOfPurchase,
        "Make": isMake,
        "Model": isModel,
        "Finance": isFinance,
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
            # could maybe send entire df for reference, for fields which need to see what others are, such as state, city, county or dob and spouse dob
            temp_data_hold = generate_col_data(column, scenario_df, i)
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

def generate_col_data(column_name, scenario_df, scenario_idx):
    if(column_name == "Gender"):
        return generate_gender(scenario_df, scenario_idx)
    # last name, first name, who cares... just generate a real lookin name using prev method...
    elif(column_name == "firstName" or column_name == "lastName" or column_name == "Spouse_First_Name" or column_name == "Spouse_Last_Name"):
        return generate_name(column_name, scenario_df, scenario_idx)
    elif(column_name == "Primary_Phone" or column_name == "Secondary_Phone"):
        return generate_phone_num()
    # should prob make sure these arent too far apart... :---0 dont wanna get weird
    elif(column_name == "DOB" or column_name == "Spouse_DOB"):
        return generate_DOB()
    elif(column_name == "Address"):
        return generate_address()
    elif(column_name == "Street_Address"):
        return generate_street_address()
    elif(column_name == "Apt"):
        return generate_apt()
    elif(column_name == "City"):
        return generate_city(scenario_df, scenario_idx)
    elif(column_name == "County"):
        return generate_county(scenario_df, scenario_idx)
    elif(column_name == "Zip"):
        return generate_zip()
    elif(column_name == "State"):
        return generate_state()
    elif(column_name == "Rent_or_Own"):
        return generate_rent_or_own()
    elif(column_name == "Email_Address"):
        return generate_email_address(scenario_df, scenario_idx)
    elif(column_name == "Date_of_Purchase"):
        return generate_data_of_purch()
    elif(column_name == "Make"):
        return generate_make()
    elif(column_name == "Model"):
        return generate_model()
    elif(column_name == "Finance"):
        return generate_finance()
    else:
        return None

# we can have a base function which checks the col we need to generate data for...
# then go on to call a helper method like this to generate tha actual data?

# gender... should probably correlate with the name... right? How will I really create that association tho? Im not going in
# labelling 10k names F or M... hmmm
###gonna try and utilize an api for classifiying name by gender
def generate_gender(scenario_df, scenario_idx):
    # jesus christ... trying to use this API to get gender for given name of a scenario, but that truly takes so long, just for 10!
    # may resort to just doing 50/50 draw either M or F... doesnt reaaaaaly matter, right? Wasted so much time tho... the option is there tho.
    # scenario_fname = scenario_df["firstName"][scenario_idx]
    # params = { "text" : scenario_fname }

    # # for dev on this limu laptop, should turn ssl verification off, just temporarily to get requests thru
    # # remove that once it is being hosted on a cloud server...
    # response = requests.request("GET", url, headers = headers, params = params, verify = False)
    # predicted_gender = json.loads(response.text)["gender"]

    # if(predicted_gender == "male"):
    #     return "M"
    # elif(predicted_gender == "female"):
    #     return "F"

    gender_chance = random.uniform(0,1)
    if(gender_chance <= .5):
        return "M"
    else:
        return "F"

###################### come back when lname csv is made #########################
def generate_name(column_name, scenario_df, scenario_idx):
    if(column_name == "firstName" or column_name == "Spouse_First_Name"):
        fname_rand_idx = random.randint(0, fname_size)
        name = fname_csv["firstname"][fname_rand_idx]
    elif(column_name == "lastName"):
        # change this to use lname csv once i generate that...
        lname_rand_idx = random.randint(0, fname_size)
        name = fname_csv["firstname"][lname_rand_idx]
    elif(column_name == "Spouse_Last_Name"):
        spouse_lname = ""
        if("lastName" in scenario_df):
            spouse_lname = scenario_df["lastName"][scenario_idx]
        else:
            # change this as well to use lname csv once its made
            lname_rand_idx = random.randint(0, fname_size)
            spouse_lname = fname_csv["firstname"][lname_rand_idx]

        name = spouse_lname

    return name

def generate_phone_num():
    phone_num_len = 10
    dummy_nummy = ""
    for i in range(1, phone_num_len + 1):
        # print(i)
        phone_diggi = str(random.randint(0,9))
        dummy_nummy += phone_diggi
        if(i % 3 == 0 and i <= 6):
            dummy_nummy += "-"

    return dummy_nummy

# this vs street address hmmmmm... probably remove one of em
def generate_address():
    return "boonky"

def generate_DOB():
    # check if isSpouse is true... if so, make the person age 18 or up.
    # also, if isSpouse is true, the delta between the DOB we generate and the spouse DOB we generate shouldnt be more than like 15yrs
    stime = datetime.date(1925, 1, 1)
    dtime = datetime.date(2002, 1, 1)

    time_between_dates = dtime - stime
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    dummy_date = stime + datetime.timedelta(days=random_number_of_days)

    return str(dummy_date)

# uhhh whats the diff between this and address??? gotta clarify
def generate_street_address():
    # need to generate some random word/name/etc plus some suffix, st/dr/blvd/etc
    return "poop st"

# not really sure about this atm... come back in future...
def generate_apt():
    return "666"

# the 3 following methods will coincide and work with each other hopefully...
def generate_state():
    # state mapping
    state_mapping = {0: 'AK', 1: 'AL', 2: 'AR', 3: 'AZ', 4: 'CA', 5: 'CO', 6: 'CT', 7: 'DE', 8: 'FL', 9: 'GA', 10: 'HI', 11: 'IA', 12: 'ID', 13: 'IL', 14: 'IN', 15: 'KS', 16: 'KY', 17: 'LA', 18: 'MA', 19: 'MD', 20: 'ME', 21: 'MI', 22: 'MN', 23: 'MO', 24: 'MS', 25: 'MT', 26: 'NC', 27: 'ND', 28: 'NE', 29: 'NH', 30: 'NJ', 31: 'NM', 32: 'NV', 33: 'NY', 34: 'OH', 35: 'OK', 36: 'OR', 37: 'PA', 38: 'RI', 39: 'SC', 40: 'SD', 41: 'TN', 42: 'TX', 43: 'UT', 44: 'VA', 45: 'VT', 46: 'WA', 47: 'WI', 48: 'WV', 49: 'WY'}
    # use map of all states? generate random digit, get whatever val has that val as a key...
    # but states should correspond to citys and coutnies should correspond to cities...
    # so may need maps for a good bit of cities in each state type map, and lists of counties in cities type map... lots of maps yeesh
    state_idx = random.randint(0,49)
    # print("state from generate_state: ", state_mapping[state_idx])
    return state_mapping[state_idx]

def generate_city(scenario_df, scenario_idx):
    # print("generated data row: ", scenario_idx)
    # choose state matching the state of the curr scenario idx, then use state to city mappings to utilize array of cities which are associated with the current state... choose random index then bingo
    city_for_state = "Nowhere"
    if("State" in scenario_df):
        # can maybe abstract out these line to a method, as we use the same lines in county generation if state is given, but city is not
        scenario_state = scenario_df["State"][scenario_idx]
        # gonna reset index of this returned df of diltered states, just so we can use the idx 0-size of filtered set properly... if not, they will keep their relative idx from the parent df
        filtered_states = location_data_csv.loc[location_data_csv["state_id"] == scenario_state].reset_index()
        specific_state_size = len(filtered_states) - 1
        random_state_idx = random.randint(0, specific_state_size)

        city_for_state = filtered_states.loc[random_state_idx]["city_ascii"]

    else:
        # print("no state for city")
        random_city_idx = random.randint(0, location_data_size)
        random_city = location_data_csv["city_ascii"][random_city_idx]
        city_for_state = random_city

    return city_for_state

def generate_county(scenario_df, scenario_idx):
    county_for_city = "Nowhere"
    # if city is checked, get the county which has a matching city, from within the chosen state - should just be 1!
    if("City" in scenario_df):
        # if city is checked, see if state is too
        # if it is, fine the county with matching state and city for the scenario
        # if not, find some rando county with matching city
        if("State" in scenario_df):
            scenario_city = scenario_df["City"][scenario_idx]
            scenario_state = scenario_df["State"][scenario_idx]
            filtered_cities_states = location_data_csv.loc[(location_data_csv["city_ascii"] == scenario_city) & (location_data_csv["state_id"] == scenario_state)].reset_index()

            county_for_city = filtered_cities_states["county_name"][0] #for some weird reason, i have to call the field name and then the index... unlike how i was doing it for city and state... weird

        else:
            scenario_city = scenario_df["City"][scenario_idx]
            filtered_cities = location_data_csv.loc[location_data_csv["city_ascii"] == scenario_city].reset_index()
            specific_city_size = len(filtered_cities) - 1
            random_city_idx = random.randint(0, specific_city_size)

            county_for_city = filtered_cities["county_name"][random_city_idx]

    # if city is not checked, then check if state is - 
    ## if state is checked, then choose a county which resides in that state 
    ## if state is also not checked, generate a completely random county...
    else:
        if("State" in scenario_df):
            scenario_state = scenario_df["State"][scenario_idx]
            filtered_states = location_data_csv.loc[location_data_csv["state_id"] == scenario_state].reset_index()
            specific_state_size = len(filtered_states) - 1
            random_state_idx = random.randint(0, specific_state_size)

            county_for_state = filtered_states.loc[random_state_idx]["county_name"]
            county_for_city = county_for_state
        else:
            random_county_idx = random.randint(0, location_data_size)
            random_county = location_data_csv["county_name"][random_county_idx]
            county_for_city = random_county

    return county_for_city

def generate_zip():
    # if i wanna be realllly true to zip codes, the lowest possible zip code is 00501... while the highest is 99950
    zip_len = 5
    dummy_zippy = ""
    for i in range(zip_len):
        zip_dig = str(random.randint(0, 9))
        dummy_zippy += zip_dig

    return dummy_zippy

def generate_rent_or_own():
    x = random.uniform(0,1)
    if(x <= .5):
        return "Rent"
    else:
        return "Own"

####### i think this is done... but check that it still is working as expected once lname csv is made! ################
def generate_email_address(scenario_df, scenario_idx):
    domains = {0: 'yahoo.com', 1: 'gmail.com', 2:'hotmail.com', 3:'bellsouth.net', 4:'comcast.net'}
    rand_dom = random.randint(0,4)

    isFName = False
    isLName = False
    fName = ""
    lName = ""

    if("lastName" in scenario_df):
        isLName = True
        lName = scenario_df["lastName"][scenario_idx]
    if("firstName" in scenario_df):
        isFName = True
        fName = scenario_df["firstName"][scenario_idx]

    if(isFName and isLName):
        email_prefix = fName[0]
        email_lName = lName
        email_user = email_prefix.lower() + email_lName + str(random.randint(1,999))
    
    elif(isFName and ~isLName):
        email_user = fName + str(random.randint(1,999))

    elif(~isFName and isLName):
        email_user = lName + str(random.randint(1,999))

    elif(~isFName and ~isLName):
        # generate random email
        rand_email_len = random.randint(4, 10)
        email_user = ''.join(random.choice(letters) for i in range(rand_email_len)) + str(random.randint(1,999))

    return email_user + "@" + domains[rand_dom]

def generate_data_of_purch():
    return "August 21st"

def generate_make():
    return "Nissan"

def generate_model():
    return "Altima"

def generate_finance():
    x = random.uniform(0,1)
    if(x <= .5):
        return "Yes"
    else:
        return "No"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug="True") #need to set host to 0,0,0,0 so it is externally visible... def might need to change in future