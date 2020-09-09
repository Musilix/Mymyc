import { ScenarioField } from '../app/scenario-field';

export class HealthcareScenario {
    private  Scenario: ScenarioField = new ScenarioField({fieldValue: "No Scenario Available"});
    private  First_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  Last_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  DOB : ScenarioField = new ScenarioField({fieldValue: false});
    private  Gender : ScenarioField = new ScenarioField({fieldValue: false});
    private  SSN : ScenarioField = new ScenarioField({fieldValue: false});
    private  Email_Address : ScenarioField = new ScenarioField({fieldValue: false});
    private  Phone_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Street_Address : ScenarioField = new ScenarioField({fieldValue: false});
    private  State : ScenarioField = new ScenarioField({fieldValue: false});
    private  Zip : ScenarioField = new ScenarioField({fieldValue: false});
    private  License_Issue_State : ScenarioField = new ScenarioField({fieldValue: false});
    private  License_Issue_Date : ScenarioField = new ScenarioField({fieldValue: false});
    private  License_Expiry_Date : ScenarioField = new ScenarioField({fieldValue: false});
    private  License_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Agency_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  Employer_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  Employment_Status : ScenarioField = new ScenarioField({fieldValue: false});
    private  Speciality_Behavioral : ScenarioField = new ScenarioField({fieldValue: false});
    private  Applying_As : ScenarioField = new ScenarioField({fieldValue: false});
    private  Broker_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Pay_Commissions_To : ScenarioField = new ScenarioField({fieldValue: false});
    private  CAQH_Provider_ID : ScenarioField = new ScenarioField({fieldValue: false});
    private  Hospital_Affiliation_State : ScenarioField = new ScenarioField({fieldValue: false});
    private  NPI_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Population_Worked_With : ScenarioField = new ScenarioField({fieldValue: false});
    private  Medicare_Certified_State : ScenarioField = new ScenarioField({fieldValue: false});
    private  PTAN_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Speciality_Medical : ScenarioField = new ScenarioField({fieldValue: false});
    private  Participating_Association : ScenarioField = new ScenarioField({fieldValue: false});
    private  Speciality_Dental : ScenarioField = new ScenarioField({fieldValue: false});
    private  Policy_ID : ScenarioField = new ScenarioField({fieldValue: false});
    private  Date_First_Consulted : ScenarioField = new ScenarioField({fieldValue: false});
    private  Physician_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  Illness : ScenarioField = new ScenarioField({fieldValue: false});
    private  Claim_Submission_Date : ScenarioField = new ScenarioField({fieldValue: false});
    private  CPT_Code : ScenarioField = new ScenarioField({fieldValue: false});
    private  Broker_Status : ScenarioField = new ScenarioField({fieldValue: false});
    private  Broker_Bonus : ScenarioField = new ScenarioField({fieldValue: false});
    private  Broker_Commission : ScenarioField = new ScenarioField({fieldValue: false});
    private  Claim_ID : ScenarioField = new ScenarioField({fieldValue: false});
    private  Total_Bill : ScenarioField = new ScenarioField({fieldValue: false});
    private  Hospital_ID : ScenarioField = new ScenarioField({fieldValue: false});
    private  Claim_Process_Date : ScenarioField = new ScenarioField({fieldValue: false});
    private  Claim_Status : ScenarioField = new ScenarioField({fieldValue: false});
    private  Plan_Type : ScenarioField = new ScenarioField({fieldValue: false});
    private  Benefits : ScenarioField = new ScenarioField({fieldValue: false});
    private  Effective_Date : ScenarioField = new ScenarioField({fieldValue: false});
    private  Amount_To_HSA : ScenarioField = new ScenarioField({fieldValue: false});

    constructor(init ?: Partial<HealthcareScenario>){
        Object.assign(this, init);
    }
}
