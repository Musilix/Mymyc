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

cars_data_src = "./static_mapping_data/makes_and_models.csv"
cars_data_csv = pd.read_csv(cars_data_src)
cars_data_size = len(cars_data_csv) - 1

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
    ext_fields = [field for field in scenario_details]
    fields = {field: scenario_details[field]["fieldValue"] for field in ext_fields if field != "Scenario"}

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
    if(column_name == "Policy_Number"):
        return generate_pol_num()
    elif(column_name == "Gender"):
        return generate_gender(scenario_df, scenario_idx)
    # last name, first name, who cares... just generate a real lookin name using prev method...
    elif(column_name == "Insured_First_Name" or column_name == "Insured_Last_Name" or column_name == "Insured_Middle_Name" or column_name == "Spouse_First_Name" or column_name == "Spouse_Last_Name"):
        return generate_name(column_name, scenario_df, scenario_idx)
    elif(column_name == "Primary_Phone" or column_name == "Secondary_Phone"):
        return generate_phone_num()
    elif(column_name == "Maritial_Status"):
        return generate_marital_status(scenario_df, scenario_idx)
    elif(column_name == "Miles_Driven_Per_Day"):
        return generate_miles_per_day()
    elif(column_name == "Days_Driven_In_A_Week"):
        return generate_days_per_week()
    elif(column_name == "Total_Miles_Per_Year"):
        return generate_miles_per_yr(scenario_df, scenario_idx)
    # should prob make sure these arent too far apart... :---0 dont wanna get weird
    elif(column_name == "DOB" or column_name == "Spouse_Dob" or column_name == "Date_Of_Birth"):
        return generate_DOB()
    elif(column_name == "Age_While_Taking_License" or column_name == "Spouse_Age_While_Taking_License"):
        return generate_age_while_take_license(scenario_df, scenario_idx)
    elif(column_name == "Vin_Number"):
        return generate_vin()
    elif(column_name == "Address"):
        return generate_address()
    elif(column_name == "Street_Address"):
        return generate_street_address(scenario_df, scenario_idx, False)
    elif(column_name == "Garage_Address"):
        return generate_garage_address(scenario_df, scenario_idx)
    elif(column_name == "Apt"):
        return generate_apt()
    elif(column_name == "City"):
        return generate_city(scenario_df, scenario_idx)
    elif(column_name == "County"):
        return generate_county(scenario_df, scenario_idx)
    elif(column_name == "Zip" or column_name == "Zip_Code"):
        return generate_zip()
    elif(column_name == "State"):
        return generate_state()
    elif(column_name == "Rent_or_Own"):
        return generate_rent_or_own()
    elif(column_name == "Email_Address"):
        return generate_email_address(scenario_df, scenario_idx)
    elif(column_name == "Date_Of_Purchase"):
        return generate_data_of_purch(scenario_df, scenario_idx)
    elif(column_name == "Employment_Status" or column_name == "Spouse_Employment_Status"):
        return generate_emp_status()
    elif(column_name == "Secondary_Driver"):
        return generate_secondary_driver()
    elif(column_name == "Safety_Device"):
        return generate_safety_dev()
    elif(column_name == "Primary_Usage"):
        return generate_prim_usage()
    elif(column_name == "Ride_Sharing_Program"):
        return generate_ride_share()
    elif(column_name == "Accident_Or_Violation_In_Past_5_Years"):
        return generate_acc_or_vio_past_5_yrs()
    elif(column_name == "Primary_Driver"):
        return generate_prim_driver()
    elif(column_name == "Bodily_Injured_Liability_Coverage"):
        return generate_bil_cov()
    elif(column_name == "Property_Damage_Liability_Coverage"):
        return generate_prop_damage_liab_cov()
    elif(column_name == "Collision_Coverage"):
        return generate_coll_cov()
    elif(column_name == "Comprehensive_Coverage"):
        return generate_comp_cov()
    elif(column_name == "Rental_Reimbursement"):
        return generate_rent_reimb()
    elif(column_name == "Make"):
        return generate_make()
    elif(column_name == "Model"):
        return generate_model(scenario_df, scenario_idx)
    elif(column_name == "Finance"):
        return generate_finance()


    elif(column_name == "Bodily_Injured_Per_Person" or column_name == "Bil_Per_Occurance"):
        # these come to have vals in the same range, so just bunch them into one
        return generate_limits_liab_deducts(50000, 500000)
    elif(column_name == "Property_Damage_Limit_Per_Occurance"):
        return generate_limits_liab_deducts(50000, 500000)
    elif(column_name == "Collision_Deductible"):
        return generate_limits_liab_deducts(10000, 300000)
    elif(column_name == "Comprehensive_Deductible"):
        return generate_limits_liab_deducts(100, 5000)
    elif(column_name == "Rental_Reimbursement_Limit"):
        return generate_rental_reimb_lim()
    else:
        return None

# we can have a base function which checks the col we need to generate data for...
# then go on to call a helper method like this to generate tha actual data?

def generate_pol_num():
    max_size = 10
    pol_num = "".join([str(random.randint(0,9)) for i in range(0, max_size)]) # trying to find hack so large numbers show up

    return pol_num

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
    if(column_name == "firstName" or column_name == "Insured_First_Name" or column_name == "Spouse_First_Name"):
        fname_rand_idx = random.randint(0, fname_size)
        name = fname_csv["firstname"][fname_rand_idx]
    elif(column_name == "lastName" or column_name == "Insured_Last_Name" or column_name == "Insured_Middle_Name"):
        # change this to use lname csv once i generate that...
        lname_rand_idx = random.randint(0, fname_size)
        name = fname_csv["firstname"][lname_rand_idx]
    elif(column_name == "Spouse_Last_Name"):
        spouse_lname = ""
        if("Insured_Last_Name" in scenario_df):
            spouse_lname = scenario_df["Insured_Last_Name"][scenario_idx]
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

def generate_marital_status(scenario_df, scenario_idx):
    marital_statuses = {0: "Married", 1: "Single", 2: "Divorced"}
    hasSpouse = False
    if("Spouse_First_Name" in scenario_df or "Spouse_Last_Name" in scenario_df or "Spouse_Dob" in scenario_df):
        hasSpouse = True

    if(hasSpouse):
        marital_status = marital_statuses[0]
    else:
        marital_idx = random.randint(0, 2)
        marital_status = marital_statuses[marital_idx]

    return marital_status

def generate_miles_per_day():
    miles_per_day = random.randint(10, 110)
    return miles_per_day

def generate_days_per_week():
    return random.randint(1,7)

def generate_miles_per_yr(scenario_df, scenario_idx):
    # if miles per day is given, see if days per week is given, to try n give a more precise val for miles per yr
    # if no days of drivin per week is given, just approximate with miles per day given
    # if neither, just generate some rando val between 1000-200000
    if("Miles_Driven_Per_Day" in scenario_df):
        miles_per_day = scenario_df["Miles_Driven_Per_Day"][scenario_idx]
        if("Days_Driven_In_A_Week" in scenario_df):
            days_per_week = scenario_df["Miles_Driven_Per_Day"][scenario_idx]
            return (miles_per_day * days_per_week) * 52
        else:
            return miles_per_day * 365
    else:
        return random.randint(1000, 200000)

# this vs street address hmmmmm... probably remove one of em
def generate_address():
    return "boonky"

def generate_garage_address(scenario_df, scenario_idx):
    address = generate_street_address(scenario_df, scenario_idx, True)
    zip_code = generate_zip()

    return address + " - " + zip_code

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

def generate_age_while_take_license(scenario_df, scenario_idx):
    # this is kinda the same as... date of purchase?
    # hmm whats really different here tho?
    # a person could of gotten a license between when they were born n current day(1-1-2020 in this case)
    # they also coulda gotten a whole car then(date of purchase...) but they would always have the license before the purchase... so, date of purchase should maybe instead rely on date of license!
    if("Date_Of_Birth" in scenario_df):
        dob_yr = scenario_df["Date_Of_Birth"][scenario_idx].split("-")[0]
        date_of_purch_delta = int(dob_yr) + 18 #get the yr person was born, add 18 yrs, as i dont think theyd have a policy up until they were at least 18
        
        stime = datetime.date(date_of_purch_delta, 1, 1)
        dtime = datetime.date(2020, 1, 1)

        time_between_dates = dtime - stime
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)

        dummy_date = stime + datetime.timedelta(days=random_number_of_days)

        return str(int(dummy_date.year) - int(dob_yr))
    else:
        rando_date = generate_DOB()
        rando_yr = rando_date.split("-")[0]

        return str(2020 - int(rando_yr))

def generate_vin():
    # set up static size of around 11, but this can go up to range to 50!
    vin_size = 17
    vin_num = ""
    for i in range(0, vin_size):
        num_or_letter = generate_yes_or_no()
        if(num_or_letter == "Yes"):
            vin_num += str(random.randint(0, 9))
        else:
            vin_num += random.choice(string.ascii_letters).capitalize()
    
    return vin_num
    
def generate_street_address(scenario_df, scenario_idx, forGarage):
    address = ""

    address_suffixes = {0: "Ave", 1: "Court", 2: "Blvd", 3: "St", 4: "Dr", 5: "Way", 6: "Sqr", 7: "Pt", 8: "Park", 9: "Ct"}
    rand_address_suffix = random.randint(0, 9)

    # get house num if apt isnt chosen
    if("Apt" not in scenario_df or forGarage):
        add_num = "".join([str(random.randint(0,9)) for i in range(1,random.randint(3,4))])
        address += (add_num + " ")
    
    # get rando county name to fill in for street name... they all look similar anyway. may want to change this in the future
    random_add_name_idx = random.randint(0, location_data_size)
    random_add_name = location_data_csv["county_name"][random_add_name_idx]
    address += random_add_name
    
    add_suff = " " + address_suffixes[rand_address_suffix]
    address += add_suff

    return address

def generate_apt():
    apt_num = int("".join([str(random.randint(0,9)) for i in range(0,4)]))
    return apt_num

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

    if("Insured_Last_Name" in scenario_df):
        isLName = True
        lName = scenario_df["Insured_Last_Name"][scenario_idx]
    if("Insured_First_Name" in scenario_df):
        isFName = True
        fName = scenario_df["Insured_First_Name"][scenario_idx]

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

def generate_data_of_purch(scenario_df, scenario_idx):
    if("Date_Of_Birth" in scenario_df):
        #aful way to get yr from date
        dob_yr = scenario_df["Date_Of_Birth"][scenario_idx].split("-")[0]
        date_of_purch_delta = int(dob_yr) + 18 #get the yr person was born, add 18 yrs, as i dont think theyd have a policy up until they were at least 18
    
        stime = datetime.date(date_of_purch_delta, 1, 1)
        dtime = datetime.date(2020, 1, 1)

        time_between_dates = dtime - stime
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)

        dummy_date = stime + datetime.timedelta(days=random_number_of_days)

        return str(dummy_date)

    else:
        return generate_DOB()

def generate_emp_status():
    # gonna test weight choices with the cool py mod...
    status = ["Employed", "Unemployed", "Self-Employed"]

    random_status = random.choices(status, weights=(60,10,30), k=1)[0]

    return random_status

def generate_secondary_driver():
    possible_drivers = ["Cousin", "Spouse", "Parent", "Child", "Grandparent", "Sibling", "None"]
    driver_weights = (10,35,10,30,5,5,5)
    random_secondary_driver = random.choices(possible_drivers, weights=driver_weights, k=1)[0]

    return random_secondary_driver

def generate_safety_dev():
    possible_safe_devs = ['Airbags', 'Antilock brakes', 'Traction control', 'Electronic stability control', 'Safety-belt features', 'Brake assist', 'Forward-collision warning', 'Automatic emergency braking', 'Pedestrian detection', 'Adaptive cruise control', 'Blind-spot warning', 'Rear cross-traffic alert', 'Lane-departure warning', 'Lane-keeping assist', 'Active head restraints', 'Backup camera', 'Tire-pressure monitors', 'Telematics']
    safe_devs_len = len(possible_safe_devs) - 1
    rand_amt_of_devices = random.randint(0, safe_devs_len)

    random_safe_devs = []
    # maybe try n come back to update this, but cant do this rn
    for i in range(0, random.randint(0, rand_amt_of_devices)):
        random_safety_dev_idx = random.randint(0, safe_devs_len)
        if(possible_safe_devs[random_safety_dev_idx] not in random_safe_devs):
            random_safe_devs.append(possible_safe_devs[random_safety_dev_idx] )

    safety_devs = "None"
    if(len(random_safe_devs) > 0):
        safety_devs = ", ".join(random_safe_devs)

    return safety_devs

def generate_prim_usage():
    # may add dependency on other fields for this... but currently, just randomly choose one
    possible_prim_usages = ['Commuting to and from work', 'Commuting to school', 'Pleasure', 'Business', 'Farm', 'Artisan']
    prim_usages_weights = (35,30,5,20,5,5)
    random_prim_usage = random.choices(possible_prim_usages, weights=prim_usages_weights, k=1)[0]

    return random_prim_usage

def generate_ride_share():
    return generate_yes_or_no()

def generate_acc_or_vio_past_5_yrs():
    return generate_yes_or_no()

def generate_prim_driver():
    return generate_yes_or_no()

def generate_bil_cov():
    return generate_yes_or_no()

def generate_prop_damage_liab_cov():
    return generate_yes_or_no()

def generate_coll_cov():
    return generate_yes_or_no()

def generate_comp_cov():
    return generate_yes_or_no()

def generate_rent_reimb():
    return generate_yes_or_no()

def generate_make():
    car_makes = {0: 'Acura', 1: 'Aston Martin', 2: 'Audi', 3: 'Bentley', 4: 'BMW', 5: 'Buick', 6: 'Cadillac', 7: 'Chevrolet', 8: 'Chrysler', 9: 'Dodge', 10: 'Ferrari', 11: 'Ford', 12: 'GMC', 13: 'Honda', 14: 'HUMMER', 15: 'Hyundai', 16: 'INFINITI', 17: 'Isuzu', 18: 'Jaguar', 19: 'Jeep', 20: 'Kia', 21: 'Lamborghini', 22: 'Land Rover', 23: 'Lexus', 24: 'Lincoln', 25: 'Lotus', 26: 'Maserati', 27: 'Maybach', 28: 'MAZDA', 29: 'Mercedes-Benz', 30: 'Mercury', 31: 'MINI', 32: 'Mitsubishi', 33: 'Nissan', 34: 'Panoz', 35: 'Pontiac', 36: 'Porsche', 37: 'Rolls-Royce', 38: 'Saab', 39: 'Saturn', 40: 'Scion', 41: 'Subaru', 42: 'Suzuki', 43: 'Toyota', 44: 'Volkswagen', 45: 'Volvo', 46: 'smart', 47: 'Ram', 48: 'FIAT', 49: 'Fisker', 50: 'McLaren', 51: 'Tesla', 52: 'Freightliner', 53: 'SRT', 54: 'Alfa Romeo', 55: 'Daihatsu', 56: 'Eagle', 57: 'Geo', 58: 'Oldsmobile', 59: 'Plymouth', 60: 'Genesis', 61: 'Rivian', 62: 'Daewoo'}
    makes_len = len(car_makes) - 1

    random_make_idx = random.randint(0, makes_len)
    random_make = car_makes[random_make_idx]

    return random_make

def generate_model(scenario_df, scenario_idx):
    if("Make" in scenario_df):
        scenario_make = scenario_df["Make"][scenario_idx]
        filtered_models = cars_data_csv.loc[cars_data_csv["make"] == scenario_make].reset_index()
        filtered_models_len = len(filtered_models) - 1

        random_model_idx = random.randint(0, filtered_models_len)

        random_model = filtered_models.loc[random_model_idx]["model"]

        return random_model

    else:
        random_model_idx = random.randint(0, cars_data_size)
        random_model = cars_data_csv.loc[random_model_idx]["model"]

        return random_model

def generate_finance():
    return generate_yes_or_no()

def generate_limits_liab_deducts(lower, upper):
    # maybe make this value weight based, so it leans more towards one side?
    lower_range = lower
    upper_range = upper

    bil = random.randrange(lower_range, upper_range)
    
    return "$" + "{:,}".format(bil)

def generate_rental_reimb_lim():
    rent_reimb_lim = ""
    low_per_day = 30
    upper_per_day = 100

    per_day_val = random.randint(low_per_day, upper_per_day)
    rent_reimb_lim += "$" + str(per_day_val) + "/day, "

    low_total = 900
    upper_total = 2500

    total_val = random.randint(low_total, upper_total)
    rent_reimb_lim += "$" + str(total_val) + " max"

    return rent_reimb_lim

def generate_yes_or_no():
    x = random.uniform(0,1)
    if(x <= .5):
        return "Yes"
    else:
        return "No"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug="True") #need to set host to 0,0,0,0 so it is externally visible... def might need to change in future