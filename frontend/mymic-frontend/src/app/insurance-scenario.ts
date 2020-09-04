import { ScenarioField } from '../app/scenario-field';

export class InsuranceScenario {
    private  Scenario: ScenarioField = new ScenarioField({fieldValue: "No Scenario Available"});
    private  Policy_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Insured_First_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  Insured_Middle_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  Insured_Last_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  Date_Of_Birth : ScenarioField = new ScenarioField({fieldValue: false});
    private  Gender : ScenarioField = new ScenarioField({fieldValue: false});
    private  Spouse_First_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  Spouse_Last_Name : ScenarioField = new ScenarioField({fieldValue: false});
    private  Spouse_Dob : ScenarioField = new ScenarioField({fieldValue: false});
    private  Maritial_Status : ScenarioField = new ScenarioField({fieldValue: false});
    private  Street_Address : ScenarioField = new ScenarioField({fieldValue: false});
    private  Apt : ScenarioField = new ScenarioField({fieldValue: false});
    private  State : ScenarioField = new ScenarioField({fieldValue: false});
    private  City : ScenarioField = new ScenarioField({fieldValue: false});
    private  County : ScenarioField = new ScenarioField({fieldValue: false});
    private  Zip_Code : ScenarioField = new ScenarioField({fieldValue: false});
    private  Email_Address : ScenarioField = new ScenarioField({fieldValue: false});
    private  Primary_Phone : ScenarioField = new ScenarioField({fieldValue: false});
    private  Secondary_Phone : ScenarioField = new ScenarioField({fieldValue: false});
    private  Age_While_Taking_License : ScenarioField = new ScenarioField({fieldValue: false});
    private  Spouse_Age_While_Taking_License : ScenarioField = new ScenarioField({fieldValue: false});
    private  Date_Of_Purchase : ScenarioField = new ScenarioField({fieldValue: false});
    private  Make : ScenarioField = new ScenarioField({fieldValue: false});
    private  Model : ScenarioField = new ScenarioField({fieldValue: false});
    private  Vin_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Finance : ScenarioField = new ScenarioField({fieldValue: false});
    private  Primary_Usage : ScenarioField = new ScenarioField({fieldValue: false});
    private  Ride_Sharing_Program : ScenarioField = new ScenarioField({fieldValue: false});
    private  Garage_Address : ScenarioField = new ScenarioField({fieldValue: false});
    private  Miles_Driven_Per_Day : ScenarioField = new ScenarioField({fieldValue: false});
    private  Days_Driven_In_A_Week : ScenarioField = new ScenarioField({fieldValue: false});
    private  Total_Miles_Per_Year : ScenarioField = new ScenarioField({fieldValue: false});
    private  Safety_Device : ScenarioField = new ScenarioField({fieldValue: false});
    private  Employment_Status : ScenarioField = new ScenarioField({fieldValue: false});
    private  Accident_Or_Violation_In_Past_5_Years : ScenarioField = new ScenarioField({fieldValue: false});
    private  Spouse_Employment_Status : ScenarioField = new ScenarioField({fieldValue: false});
    private  Primary_Driver : ScenarioField = new ScenarioField({fieldValue: false});
    private  Secondary_Driver : ScenarioField = new ScenarioField({fieldValue: false});
    private  Bodily_Injured_Liability_Coverage : ScenarioField = new ScenarioField({fieldValue: false});
    private  Bodily_Injured_Per_Person : ScenarioField = new ScenarioField({fieldValue: false});
    private  Bil_Per_Occurance : ScenarioField = new ScenarioField({fieldValue: false});
    private  Property_Damage_Liability_Coverage : ScenarioField = new ScenarioField({fieldValue: false});
    private  Property_Damage_Limit_Per_Occurance : ScenarioField = new ScenarioField({fieldValue: false});
    private  Collision_Coverage : ScenarioField = new ScenarioField({fieldValue: false});
    private  Collision_Deductible : ScenarioField = new ScenarioField({fieldValue: false});
    private  Comprehensive_Coverage : ScenarioField = new ScenarioField({fieldValue: false});
    private  Comprehensive_Deductible : ScenarioField = new ScenarioField({fieldValue: false});
    private  Rental_Reimbursement : ScenarioField = new ScenarioField({fieldValue: false});
    private  Rental_Reimbursement_Limit : ScenarioField = new ScenarioField({fieldValue: false});

    constructor(init ?: Partial<InsuranceScenario>){
        Object.assign(this, init);
    }
}
