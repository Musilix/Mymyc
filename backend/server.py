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
fname_size = len(fname_csv) - 1

# either make a csv for lnames or combine the two and edit var names

# need data source for city state county mappings
location_data_src = "./static_mapping_data/states_to_cities_to_counties.csv"
location_data_csv = pd.read_csv(location_data_src)
# keep global ref to size of this location csv
location_data_size = len(location_data_csv) - 1

cars_data_src = "./static_mapping_data/makes_and_models.csv"
cars_data_csv = pd.read_csv(cars_data_src)
cars_data_size = len(cars_data_csv) - 1

employers_data_src = "./static_mapping_data/employers.csv"
employers_data_csv = pd.read_csv(employers_data_src)
employers_data_len = len(employers_data_csv) - 1

bank_names_src = "./static_mapping_data/bank_names.csv"
bank_names_csv = pd.read_csv(bank_names_src)
bank_names_len = len(bank_names_csv) - 1

#DE was the only one with no definite delta... as it is every odd numbered years... so we will just make it 3
license_deltas = {'AR': 1, 'DE': 3, 'AL': 1, 'LA': 1, 'SD': 1, 'WI': 1, 'WA': 1, 'AK': 2, 'AZ': 2, 'CA': 2, 'CO': 2, 'CT': 2, 'DC': 2, 'FL': 2, 'GA': 2, 'HI': 2, 'IA': 2, 'ID': 2, 'IN': 2, 'KS': 2, 'MA': 2, 'MD': 2, 'ME': 2, 'MO': 2, 'MS': 2, 'MT': 2, 'NE': 2, 'NH': 2, 'NJ': 2, 'NV': 2, 'NY': 2, 'OH': 2, 'OR': 2, 'PA': 2, 'SC': 2, 'TX': 2, 'TN': 2, 'RI': 2, 'UT': 2, 'VT': 2, 'VA': 2, 'WV': 2, 'IL': 3, 'KY': 3, 'MI': 3, 'MN': 3, 'NC': 3, 'ND': 3, 'NM': 3, 'OK': 3, 'WY': 3}


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
    elif(column_name == "Insured_First_Name" or column_name == "Insured_Last_Name" or column_name == "Insured_Middle_Name" or column_name == "Spouse_First_Name" or column_name == "Spouse_Last_Name" or column_name == "First_Name" or column_name == "Last_Name" or column_name == "Physician_Name"):
        return generate_name(column_name, scenario_df, scenario_idx)
    elif(column_name == "Primary_Phone" or column_name == "Secondary_Phone" or column_name == "Phone_Number"):
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
    elif(column_name == "State" or column_name == "License_Issue_State" or column_name == "Hospital_Affiliation_State"):
        return generate_state()
    elif(column_name == "Rent_or_Own"):
        return generate_rent_or_own()
    elif(column_name == "Email_Address"):
        return generate_email_address(scenario_df, scenario_idx)
    elif(column_name == "Date_Of_Purchase"):
        return generate_data_of_purch(scenario_df, scenario_idx)
    elif(column_name == "Employment_Status" or column_name == "Spouse_Employment_Status"):
        return generate_emp_status(scenario_df, scenario_idx)
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
    elif(column_name == "SSN"):
        return generate_ssn()
    elif(column_name == "Pay_Commissions_To"):
        return generate_pay_comm_to()
    elif(column_name == "Speciality_Behavioral"):
        return generate_behavioral_spec()
    elif(column_name == "Applying_As"):
        return generate_apply_as()
    elif(column_name == "Population_Worked_With"):
        return generate_pop_worked_with()
    elif(column_name == "Speciality_Medical"):
        return generate_med_spec()
    elif(column_name == "Participating_Association"):
        return generate_participating_assoc()
    elif(column_name == "Speciality_Dental"):
        return generate_dental_spec()
    elif(column_name == "Policy_ID"):
        return generate_pol_id()
    elif(column_name == "Physician_Name"):
        return generate_phys_name()
    elif(column_name == "Illness"):
        return generate_illness()
    elif(column_name == "CPT_Code"):
        return generate_cpt_code()
    elif(column_name == "Amount_To_HSA"):
        return generate_amt_to_hsa()
    elif(column_name == "Broker_Bonus"):
        return generate_broker_bonus()
    elif(column_name == "Broker_Commission"):
        return generate_broker_comm()
    elif(column_name == "Claim_ID"):
        return generate_claim_id()
    elif(column_name == "Total_Bill"):
        return generate_tot_bill()
    elif(column_name == "Hospital_ID"):
        return generate_hospital_id()
    elif(column_name == "Claim_Status"):
        return generate_claim_status()
    elif(column_name == "Broker_Number"):
        return generate_brok_num()
    elif(column_name == "CAQH_Provider_ID"):
        return generate_caqh_id()
    elif(column_name == "NPI_Number"):
        return generate_npi_num()
    elif(column_name == "PTAN_Number"):
        return generate_ptan_num()
    elif(column_name == "Employer_Name"):
        return generate_emp_name(scenario_df, scenario_idx)
    elif(column_name == "Benefits"):
        return generate_benefits()
    elif(column_name == "Broker_Status"):
        return generate_broker_status()
    elif(column_name == "Plan_Type"):
        return generate_plan_type()
    elif(column_name == "Agency_Name"):
        return generate_agency_name()
    elif(column_name == "Medicare_Certified_State"):
        return generate_medicare_state()
    elif(column_name == "License_Number"):
        return generate_lic_num()
    elif(column_name == "License_Issue_Date"):
        return generate_lic_iss_date(scenario_df, scenario_idx)
    elif(column_name == "License_Expiry_Date"):
        return generate_lic_exp_date(scenario_df, scenario_idx)

  # to do
    elif(column_name == "Date_First_Consulted"):
        return generate_date_first_consulted()
    elif(column_name == "Claim_Submission_Date"):
        return generate_claim_sub_date()
    elif(column_name == "Claim_Process_Date"):
        return generate_claim_proc_date()
    elif(column_name == "Effective_Date"):
        return generate_eff_date()



    #BANKING COL HANDLERS
    elif(column_name == "Account"):
        return generate_acc()
    elif(column_name == "Account_Holder"):
        return generate_acc_holder(scenario_df, scenario_idx)
    elif(column_name == "Account_Identifier"):
        return generate_acc_id()
    
    #do these 2 have specific format
    elif(column_name == "Account_Number"):
        return generate_acc_num()
    elif(column_name == "Bank_Routing_Number"):
        return generate_route_num()

    elif(column_name == "Account_Balance"):
        return generate_acc_bal()
    elif(column_name == "Account_Specific_Service_Agreement"):
        return generate_acc_spec_serv_agree()
    elif(column_name == "Accrual"):
        return generate_accrual()
    elif(column_name == "Amortization"):
        return generate_amor()
    elif(column_name == "Amortization_Schedule"):
        return generate_amor_sched()
    elif(column_name == "Bank"):
        return generate_bank()
    elif(column_name == "Bank_Account"):
        return generate_bank_acc()
    elif(column_name == "Bank_Account_Identifier"):
        return generate_bank_acc_id()
    elif(column_name == "Banking_Product"):
        return generate_banking_prod()
    elif(column_name == "Banking_Service"):
        return generate_banking_serv()
    elif(column_name == "Borrower"):
        return generate_borrower(scenario_df, scenario_idx)
    elif(column_name == "Borrowing_Capacity"):
        return generate_borrow_cap()
    elif(column_name == "Clearing_Bank"):
        return generate_clearing_bank()
    elif(column_name == "Collateral"):
        return generate_collateral()
    elif(column_name == "Credit_Agreement"):
        return generate_cred_agreemnt()
    elif(column_name == "Credit_Card_Number"):
        return generate_cred_card_num()
    elif(column_name == "Credit_Card_Type"):
        return generate_cred_card_type()

    elif(column_name == "Credit_Card_Expiry"):
        return "Blank"
    elif(column_name == "Credit_Card_Cvv"):
        return "Blank"
    elif(column_name == "Check_Number"):
        return "Blank"
    elif(column_name == "Check_Dated"):
        return "Blank"
    elif(column_name == "Check_Deposited_Date"):
        return "Blank"
    elif(column_name == "Check_Deposit_Type"):
        return "Blank"
    elif(column_name == "Check_Type"):
        return "Blank"
    elif(column_name == "MICR_Code"):
        return "Blank"
    elif(column_name == "Date"):
        return "Blank"
    elif(column_name == "Time_Stamp"):
        return "Blank"
    elif(column_name == "Debit_Card_Number"):
        return "Blank"
    elif(column_name == "Debit_Card_Type"):
        return "Blank"
    elif(column_name == "Debit_Card_Expiry"):
        return "Blank"
    elif(column_name == "Debit_Card_Cvv"):
        return "Blank"
    elif(column_name == "Fixed_Interest_Rate"):
        return "Blank"
    elif(column_name == "Floating_Interest_Rate"):
        return "Blank"
    elif(column_name == "Full_Amortization"):
        return "Blank"
    elif(column_name == "Holding"):
        return "Blank"
    elif(column_name == "Holding_Company"):
        return "Blank"
    elif(column_name == "Insurance_Company"):
        return "Blank"
    elif(column_name == "Insurance_Policy"):
        return "Blank"
    elif(column_name == "Insurance_Service"):
        return "Blank"
    elif(column_name == "Interest"):
        return "Blank"
    elif(column_name == "Interest_Payment_Terms"):
        return "Blank"
    elif(column_name == "Interest_Rate"):
        return "Blank"
    elif(column_name == "International_Bank_Account_Identifier"):
        return "Blank"
    elif(column_name == "Investment_Account"):
        return "Blank"
    elif(column_name == "Investment_Bank"):
        return "Blank"
    elif(column_name == "Investment_Company"):
        return "Blank"
    elif(column_name == "Investment_Or_Deposit_Account"):
        return "Blank"
    elif(column_name == "Investment_Service"):
        return "Blank"
    elif(column_name == "Jurisdiction"):
        return "Blank"
    elif(column_name == "Legal_Agent"):
        return "Blank"
    elif(column_name == "Lender"):
        return "Blank"
    elif(column_name == "Loan_Or_Credit_Account"):
        return "Blank"
    elif(column_name == "Managed_Interest_Rate"):
        return "Blank"
    elif(column_name == "Payment_Service"):
        return "Blank"
    elif(column_name == "Policyholder"):
        return "Blank"
    elif(column_name == "Transaction_Type"):
        return "Blank"
    elif(column_name == "Transaction_Amount"):
        return "Blank"
    elif(column_name == "Transaction_ID"):
        return "Blank"
    elif(column_name == "Transaction_Mode"):
        return "Blank"
    elif(column_name == "Principal"):
        return "Blank"

    else:
        return "NA - error occurred"

#need to prob abstract out the process of choosing a random val from a map, as I continue to do it again n again... maybe make basic helepr method that takes map, and size, and returns random val from it

# we can have a base function which checks the col we need to generate data for...
# then go on to call a helper method like this to generate tha actual data?
def get_val_from_dict(dict, dict_len):
    dict_choice = random.randint(0, dict_len -1)

    return dict[dict_choice]

def generate_id(id_len, id_low_range, id_high_range):
    id = "".join([str(random.randint(id_low_range, id_high_range)) for i in range(0, id_len)])

    return "_" + id

def generate_lump(lower_range, upper_range):
    lump_val = random.randrange(lower_range, upper_range)
    
    return "$" + "{:,}".format(lump_val)

def generate_date(lower, upper):
    # 0 - yr, 1 - mth, 2 - day
    stime = datetime.date(lower[0], lower[1], lower[2])
    dtime = datetime.date(upper[0], upper[1], upper[2])

    time_between_dates = dtime - stime
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    dummy_date = stime + datetime.timedelta(days=random_number_of_days)

    return str(dummy_date)

def generate_iss_date(state):
    possible_issuance = license_deltas[state]

    curr_date = datetime.datetime.now()
    frthst_date = curr_date - datetime.timedelta(weeks=(44 * possible_issuance)) 

    curr_yr = curr_date.year
    curr_mth = curr_date.month
    curr_day = curr_date.day
    upr = [curr_yr, curr_mth, curr_day]

    frthst_yr = frthst_date.year
    frthst_mth = frthst_date.month
    frthst_day = frthst_date.day
    lwr = [frthst_yr, frthst_mth, frthst_day]

    return lwr,upr

def generate_collateral():
    collaterals = {0: 'Home', 1: 'Office', 2: 'Ranch', 3: 'Farm', 4: 'Car', 5: 'Truck'}
    rand_coll_idx = random.randint(0, len(collaterals) - 1)
    return collaterals[rand_coll_idx]

def generate_clearing_bank():
    return generate_bank()

def generate_borrow_cap():
    rand_bal = -1
    while(rand_bal < 0):
        rand_bal = np.random.normal(500000, 1000000, 1)

    return "$" + "{:,}".format(int(rand_bal))

def generate_borrower(scenario_df, scenario_idx):
    return generate_emp_name(scenario_df, scenario_idx)

def generate_banking_serv():
    banking_servs = {0: 'Cash Management Service', 1: 'Foreign Exchange Service', 2: 'Lending/Credit Service', 3: 'Investment Service', 4: 'Insurance Service', 5: 'Merchant Service'}
    rand_bank_serv_idx = random.randint(0, len(banking_servs) - 1)
    return banking_servs[rand_bank_serv_idx]

def generate_banking_prod():
    banking_prods = {0: 'Checking Account', 1: 'Savings Account', 2: 'Certificate Of Deposit', 3: 'Debit', 4: 'Pre-Paid Card', 5: 'Credit Card'}
    rand_bank_prod_idx = random.randint(0, len(banking_prods) - 1)
    return banking_prods[rand_bank_prod_idx]

def generate_bank_acc_id():
    return generate_id(16, 0, 9)

def generate_bank():
    rand_bank_idx = random.randint(0, bank_names_len)
    return bank_names_csv['name'][rand_bank_idx]

#maybe base this off acc bal and amor amt?
def generate_amor_sched():
    amor_multiple = random.randint(0,11) #uhhhh r these mths, weeks, yrs??? assuming mths... will someone ever have amortization sched for 11 yrs???
    return str(12 + (12 * amor_multiple))

def generate_amor():
    rand_bal = -1
    while(rand_bal < 0):
        rand_bal = np.random.normal(50000, 35000, 1)

    return "$" + "{:,}".format(int(rand_bal))

#generate interest
#just generate another balance type var... dont have any rl trends to work off of in forming a realistic accrual
def generate_accrual():
    rand_bal = np.random.normal(5000, 750, 1)
    return "$" + "{:,}".format(int(rand_bal)) 

#dependent on if there are multiple accs with the client, and varying t&c between those accs... nto rlly sure if that can be deduce with other scenario fields, so just gen random yes/no for now
def generate_acc_spec_serv_agree():
    return generate_yes_or_no()

def generate_acc_bal():
    #maybe create gausian dist of avg savings???
    rand_bal = np.random.normal(8000, 4000, 1)
    return "$" + "{:,}".format(int(rand_bal))

#curr just gen random num, as there doesnt seem to be any other field related to geolocation... so we cant deduce sections of the routing num
def generate_route_num():
    return generate_id(9, 0, 9)

def generate_acc_num():
    return generate_id(16, 0, 9)

def generate_acc_id():
    return generate_id(10, 0, 9)

def generate_acc():
    acc_types = {0: 'Personal Banking', 1: 'Professional Banking', 2: 'Investment Banking', 3: 'Retail Banking'}
    rand_acc_idx = random.randint(0, len(acc_types) - 1)
    return acc_types[rand_acc_idx]

def generate_acc_holder(scenario_df, scenario_idx):
    fname = generate_name("firstName", scenario_df, scenario_idx)
    lname = generate_name("lastName", scenario_df, scenario_idx) #change to use last_name in future

    return fname + " " + lname

#As it curr stands, the following three methods... as well as the 4th one need some more clarification
#what are the typical ranges?
#are any of them dependent on another?
#etc
def generate_claim_sub_date():
    return generate_date_first_consulted()

def generate_claim_proc_date():
    return generate_date_first_consulted()

def generate_eff_date():
    return generate_date_first_consulted()

def generate_date_first_consulted():
    lwr = [2019, 1, 1]
    upr = [datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day]

    return generate_date(lwr, upr)

#this seems kinda pointless... if it will always be single, y have it???
def generate_plan_type():
    return "Single"

#choose random or use stats on most used agencies to determine?
def generate_agency_name():
    agencies = {0: 'iHealthBrokers ', 1: 'Aetna', 2: 'United Healthcare', 3: 'Blue Cross Blue Shield', 4: 'Humana', 5: 'HealthMarkets Insurance', 6: 'Health Insurance Marketplace', 7: 'Kaiser foundation', 8: 'Cigna', 9: 'Anthem Inc.'}
    agencies_len = len(agencies) - 1

    rand_idx = random.randint(0, agencies_len)

    return agencies[rand_idx]

def generate_lic_num():
    med_lic_prefixes = {} #possiby choose from some prefixes in the future... MD, PY, etc
    lic_num_prefix = "".join([random.choice(string.ascii_letters).capitalize() for i in range(0,2)])
    lic_num_suffix = "".join([str(random.randint(0,9)) for i in range(0,7)])

    return lic_num_prefix + lic_num_suffix

def generate_lic_iss_date(scenario_df, scenario_idx):
    if("License_Issue_State" in scenario_df):
        iss_state = scenario_df["License_Issue_State"][scenario_idx]
        lwr, upr = generate_iss_date(iss_state)
        musta_been_issued_on = generate_date(lwr, upr)

        return musta_been_issued_on

    #if License_Issue_State isnt checked for the scenario, then just choose a random one fro mour dict
    else:
        # get random state and get its exp delta
        rand_iss_state = random.choice(list(license_deltas.keys()))
        lwr, upr = generate_iss_date(rand_iss_state)
        musta_been_issued_on = generate_date(lwr, upr)

        return musta_been_issued_on

def generate_lic_exp_date(scenario_df, scenario_idx):
    #if an iss date is given, check if a iss state is also given
    ### if it is, then add that states iss lifetime to the iss date to get the exp date
    ### if not, grab a random iss lifetime from the iss lifetime dict... this does... kinda cause problems tho, if the iss date was also decided this way... there will be diff iss lifetimes grabbed in all likelihood
    if("License_Issue_Date" in scenario_df):
        iss_date = datetime.datetime.strptime(scenario_df["License_Issue_Date"][scenario_idx], "%Y-%m-%d")

        if("License_Issue_State" in scenario_df):
            iss_state = scenario_df["License_Issue_State"][scenario_idx]
            issuance_delta = license_deltas[iss_state]

            exp_date = iss_date + datetime.timedelta(weeks=52 * issuance_delta)

            return str(exp_date.date())

        else:
            #the state we use here for delta will be diff from the one use in the rand state iss... seeing as we use random.choice each time... so there wont be any concise
            #iss/exp dates for scenarios with no lic iss state... hmmmm
            rand_iss_state = random.choice(list(license_deltas.keys()))
            issuance_delta = license_deltas[rand_iss_state]

            exp_date = iss_date + datetime.timedelta(weeks=52 * issuance_delta)

            return str(exp_date.date())
    #if no iss date is given, stil do a check to see if iss state is;
    ### if it is, then use that states iss lifetime to form an exp date,
    ### if not, then just grab a random iss lifetime from our dict
    else:
        if("License_Issue_State" in scenario_df):
            iss_state = scenario_df["License_Issue_State"][scenario_idx]
            issuance_delta = license_deltas[iss_state]
            exp_date = datetime.datetime.now() + datetime.timedelta(weeks=52 * issuance_delta + (random.randint(1, 25) * random.choice((-1,1))))

            return str(exp_date.date())
        else:
            rand_iss_state = random.choice(list(license_deltas.keys()))
            issuance_delta = license_deltas[rand_iss_state]

            exp_date = datetime.datetime.now() + datetime.timedelta(weeks=52 * issuance_delta + (random.randint(1, 25) * random.choice((-1,1))))

            return str(exp_date.date())

#may have to add conditional check on state in future...
def generate_medicare_state():
    return generate_yes_or_no()

# maybe have to add condition checks + weights on choice
def generate_broker_status():
    choice = generate_yes_or_no()
    if(choice == "Yes"):
        return "Active"
    else:
        return "Inactive"

def generate_emp_name(scenario_df, scenario_idx):
    if("State" in scenario_df):
        scenario_state = scenario_df["State"][scenario_idx]
        filtered_employers = employers_data_csv.loc[employers_data_csv['state_code'] == scenario_state].reset_index()
        specific_emp_len = len(filtered_employers) - 1
        rand_emp = random.randint(0, specific_emp_len)

        employer = filtered_employers.loc[rand_emp]['name']

        return employer

    else:
        random_emp_idx = random.randint(0, employers_data_len)
        random_emp = employers_data_csv["name"][random_emp_idx]
        employer = random_emp

        return employer

# possibly need to come back to add formatting rules
def generate_caqh_id():
    return generate_id(8, 0 ,9)

# possibly need to come back to add formatting rules
def generate_brok_num():
    return generate_id(9, 0, 9)

# possibly need to come back to add formatting rules
def generate_npi_num():
    return generate_id(10, 0, 9)

def generate_ptan_num():
    return generate_id(6,0,9)

def generate_amt_to_hsa():
    return generate_lump(1,100)

def generate_benefits():
    possible_benefits = {0: "Medical", 1: "HSA", 2: "Dental", 3: "Vision"}
    benefits_len = len(possible_benefits) - 1
    rand_amt_of_benefits = random.randint(0, benefits_len)

    random_benefits = []

    for i in range(0, rand_amt_of_benefits):
        random_benefit_idx = random.randint(0, benefits_len)
        if(possible_benefits[random_benefit_idx] not in random_benefits):
            random_benefits.append(possible_benefits[random_benefit_idx])

    benefits = "None"
    if(len(random_benefits) > 0):
        benefits = ", ".join(random_benefits)

    return benefits

def generate_broker_bonus():
    return generate_lump(1, 1000)

def generate_broker_comm():
    return generate_lump(1, 10000)

# possibly need to come back to add formatting rules
def generate_claim_id():
    return generate_id(9, 0, 9)

def generate_tot_bill():
    return generate_lump(1, 10000)

# possibly need to come back to add formatting rules
def generate_hospital_id():
    return generate_id(9, 0, 9)

def generate_claim_status():
    statuses = {0: "In Progress", 1: "Accepted", 2: "Rejected"}
    return get_val_from_dict(statuses, len(statuses))

def generate_cpt_code():
    return generate_id(5, 0, 9)

def generate_illness():
    illnesses = {0: 'Fever', 1: 'Surgery', 2: 'Viral', 3: 'Other', 4: 'Fracture'}

    return get_val_from_dict(illnesses, len(illnesses))

def generate_pol_id():
    return generate_id(15, 0, 9)

def generate_dental_spec():
    dental_specs = {0: 'General Dentist', 1: 'Oral Surgeon', 2: 'Pedodontist', 3: 'Endodontist', 4: 'Other'}

    return get_val_from_dict(dental_specs, len(dental_specs))

def generate_participating_assoc():
    associations = {0: 'DBO', 1: 'PPO'}

    return get_val_from_dict(associations, len(associations))

def generate_med_spec():
    med_specs = {0: 'Neurology', 1: 'Endocrenology', 2: 'Dermatology', 3: 'Cardiology', 4: 'Pathology', 5: 'Pediatrics', 6: 'Others'}

    return get_val_from_dict(med_specs, len(med_specs))

def generate_pop_worked_with():
    pops = ['35 and under', '36-45', '46-55', '56-65', '66+']
    pop_likeliness = (11.2, 19.8, 22.9, 29, 17)

    pop_worked_with = random.choices(pops, weights=pop_likeliness, k=1)[0]

    return pop_worked_with

def generate_apply_as():
    apply_spec = {0: 'Specialist', 1: 'Primary Care Physician', 2: 'Allied'}
    apply_as_choice = random.randint(0, len(apply_spec) -1)

    return apply_spec[apply_as_choice]

def generate_behavioral_spec():
    behavioral_specs = {0: 'Child Psychiatry', 1: 'Clinical Psychology', 2: 'Psychiatric Nurse', 3: 'Other'}
    spec_choice = random.randint(0, len(behavioral_specs) - 1)

    return behavioral_specs[spec_choice]

def generate_pay_comm_to():
    recipients = {0: "Broker", 1: "Agent"}
    recipient_choice = random.randint(0,1)

    return recipients[recipient_choice]

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
    name = "Jane Doe"
    if(column_name == "firstName" or column_name == "Insured_First_Name" or column_name == "Spouse_First_Name" or column_name == "First_Name" or column_name == "Physician_Name"):
        fname_rand_idx = random.randint(0, fname_size)
        name = fname_csv["firstname"][fname_rand_idx]
    elif(column_name == "lastName" or column_name == "Insured_Last_Name" or column_name == "Last_Name" or column_name == "Insured_Middle_Name"):
        # change this to use lname csv once i generate that...
        lname_rand_idx = random.randint(0, fname_size)
        name = fname_csv["firstname"][lname_rand_idx]
    elif(column_name == "Spouse_Last_Name"):
        spouse_lname = ""
        if("Insured_Last_Name" in scenario_df):
            spouse_lname = scenario_df["Insured_Last_Name"][scenario_idx]
        elif("Last_Name" in scenario_df):
            spouse_lname = scenario_df["Last_Name"][scenario_idx]
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

#use weihts maybe?
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

def generate_garage_address(scenario_df, scenario_idx):
    address = generate_street_address(scenario_df, scenario_idx, True)
    zip_code = generate_zip()

    return address + " - " + zip_code

# probably should do something with this
def generate_DOB():
    # check if isSpouse is true... if so, make the person age 18 or up.
    # also, if isSpouse is true, the delta between the DOB we generate and the spouse DOB we generate shouldnt be more than like 15yrs

    # percentage of ppl by age
    birth_ranges = [(18, 24), (25,44), (45,64), (65, 80), (81, 99)]
    age_whts = (9.6, 30.2, 22, 12.4, 5.8)

    chc = random.choices(birth_ranges, weights=age_whts, k=1)[0]

    curr_yr = datetime.datetime.now().year

    lwr_bound = curr_yr - chc[1]
    upr_bound = curr_yr - chc[0]


    stime = datetime.date(lwr_bound, 1, 1)
    dtime = datetime.date(upr_bound, 1, 1)

    time_between_dates = dtime - stime
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    dummy_date = stime + datetime.timedelta(days=random_number_of_days)

    return str(dummy_date)

# this is kinda the same as... date of purchase?
# hmm whats really different here tho?
# a person could of gotten a license between when they were born n current day(1-1-2020 in this case)
# they also coulda gotten a whole car then(date of purchase...) but they would always have the license before the purchase... so, date of purchase should maybe instead rely on date of license!
def generate_age_while_take_license(scenario_df, scenario_idx):
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

# may need to add check that vin is unique
# update logic for VIN generation 
# should vin be consistent with geo details(state,county,city)? and make/model? for now, just make sure it looks rl, but not consistent yet
def generate_vin():
    vin_size = 17
    vin_manu_sect = "" #first 3 digits
    vin_desc_sect = "" #4th thru 9th digits
    vin_ident_sect = "" #10th thru 17th digits

    # for i in range(0,3):
    #     if(i == 0):
    #         num_or_letter = generate_yes_or_no()
    #         if(num_or_letter == "Yes"):
    #             vin_num += str(random.randint(0, 9))
    #         else:
    #             vin_num += random.choice(string.ascii_letters).capitalize()

    vin_num = ""
    for i in range(0, vin_size):
        num_or_letter = generate_yes_or_no()
        if(num_or_letter == "Yes"):
            vin_num += str(random.randint(1, 9))
        else:
            vin_num += random.choice(string.ascii_letters).capitalize()
    
    return vin_num
    
def generate_street_address(scenario_df, scenario_idx, forGarage):
    address = ""

    address_suffixes = {0: "Ave", 1: "Court", 2: "Blvd", 3: "St", 4: "Dr", 5: "Way", 6: "Sqr", 7: "Pt", 8: "Park", 9: "Ct"}
    rand_address_suffix = random.randint(0, 9)

    # get house num if apt isnt chosen
    if("Apt" not in scenario_df or forGarage):
        add_num = "".join([str(random.randint(1,9)) for i in range(1,random.randint(3,4))])
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
    if("Last_Name" in scenario_df):
        isLName = True
        lName = scenario_df["Last_Name"][scenario_idx]
    if("First_Name" in scenario_df):
        isFName = True
        fName = scenario_df["First_Name"][scenario_idx]

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

def generate_emp_status(scenario_df, scenario_idx):
    if("Employer_Name" in scenario_df):
        return "Employed"
    else:
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

# may need to add check that ssn generated is unique
def generate_ssn():
    first_sec = ""
    midd_sec = ""
    final_sec = ""

    # generate 1st section
    for i in range(0,3):
        # make sure we dont get three 0s in a row
        if(len(first_sec) == 2):
            if(first_sec == "00"):
                rando_digit = random.randint(1,9)
                first_sec += str(rando_digit)
            elif(first_sec == "66"):
                rando_digit = random.randint(0,9)
                while(rando_digit == "6"):
                    rando_digit = random.randint(0,9)
                
                first_sec += str(rando_digit)
            else:
                rando_digit = random.randint(0,9)
                first_sec += str(rando_digit)
        else:
            rando_digit = random.randint(0,9)
            first_sec += str(rando_digit)
    
    # generate midd section
    for i in range(0,2):
        if(len(midd_sec) == 1):
            rando_digit = random.randint(1,9)
            midd_sec += str(rando_digit)
        else:
            rando_digit = random.randint(0,9)
            midd_sec += str(rando_digit)

    # generate final section
    for i in range(0, 4):
        if(len(final_sec) == 3):
            rando_digit = random.randint(1, 9)
            final_sec += str(rando_digit)
        else:
            rando_digit = random.randint(0,9)
            final_sec += str(rando_digit)

    # concatanate
    ssn =  first_sec + "-" + midd_sec + "-" + final_sec 
    return ssn

def generate_yes_or_no():
    x = random.uniform(0,1)
    if(x <= .5):
        return "Yes"
    else:
        return "No"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug="True") #need to set host to 0,0,0,0 so it is externally visible... def might need to change in future