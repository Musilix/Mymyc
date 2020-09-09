import {ScenarioField} from './scenario-field';

//is there... a simpler way of doing this shit? Reading in from a file perhaps and using a script to create these vars?
export class BankingScenario {
    private  Scenario: ScenarioField = new ScenarioField({fieldValue: "No Scenario Available"});
    private  Account : ScenarioField = new ScenarioField({fieldValue: false});
    private  Account_Holder : ScenarioField = new ScenarioField({fieldValue: false});
    private  Account_Identifier : ScenarioField = new ScenarioField({fieldValue: false});
    private  Account_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Bank_Routing_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Account_Balance : ScenarioField = new ScenarioField({fieldValue: false});
    private  Account_Specific_Service_Agreement : ScenarioField = new ScenarioField({fieldValue: false});
    private  Accrual : ScenarioField = new ScenarioField({fieldValue: false});
    private  Amortization : ScenarioField = new ScenarioField({fieldValue: false});
    private  Amortization_Schedule : ScenarioField = new ScenarioField({fieldValue: false});
    private  Bank : ScenarioField = new ScenarioField({fieldValue: false});
    private  Bank_Account : ScenarioField = new ScenarioField({fieldValue: false});
    private  Bank_Account_Identifier : ScenarioField = new ScenarioField({fieldValue: false});
    private  Banking_Product : ScenarioField = new ScenarioField({fieldValue: false});
    private  Banking_Service : ScenarioField = new ScenarioField({fieldValue: false});
    private  Borrower : ScenarioField = new ScenarioField({fieldValue: false});
    private  Borrowing_Capacity : ScenarioField = new ScenarioField({fieldValue: false});
    private  Clearing_Bank : ScenarioField = new ScenarioField({fieldValue: false});
    private  Collateral : ScenarioField = new ScenarioField({fieldValue: false});
    private  Credit_Agreement : ScenarioField = new ScenarioField({fieldValue: false});
    private  Credit_Card_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Credit_Card_Type : ScenarioField = new ScenarioField({fieldValue: false});
    private  Credit_Card_Expiry : ScenarioField = new ScenarioField({fieldValue: false});
    private  Credit_Card_Cvv : ScenarioField = new ScenarioField({fieldValue: false});
    private  Check_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Check_Dated : ScenarioField = new ScenarioField({fieldValue: false});
    private  Check_Deposited_Date : ScenarioField = new ScenarioField({fieldValue: false});
    private  Check_Deposit_Type : ScenarioField = new ScenarioField({fieldValue: false});
    private  Check_Type : ScenarioField = new ScenarioField({fieldValue: false});
    private  MICR_Code : ScenarioField = new ScenarioField({fieldValue: false});
    private  Date : ScenarioField = new ScenarioField({fieldValue: false});
    private  Time_Stamp : ScenarioField = new ScenarioField({fieldValue: false});
    private  Debit_Card_Number : ScenarioField = new ScenarioField({fieldValue: false});
    private  Debit_Card_Type : ScenarioField = new ScenarioField({fieldValue: false});
    private  Debit_Card_Expiry : ScenarioField = new ScenarioField({fieldValue: false});
    private  Debit_Card_Cvv : ScenarioField = new ScenarioField({fieldValue: false});
    private  Fixed_Interest_Rate : ScenarioField = new ScenarioField({fieldValue: false});
    private  Floating_Interest_Rate : ScenarioField = new ScenarioField({fieldValue: false});
    private  Full_Amortization : ScenarioField = new ScenarioField({fieldValue: false});
    private  Holding : ScenarioField = new ScenarioField({fieldValue: false});
    private  Holding_Company : ScenarioField = new ScenarioField({fieldValue: false});
    private  Insurance_Company : ScenarioField = new ScenarioField({fieldValue: false});
    private  Insurance_Policy : ScenarioField = new ScenarioField({fieldValue: false});
    private  Insurance_Service : ScenarioField = new ScenarioField({fieldValue: false});
    private  Interest : ScenarioField = new ScenarioField({fieldValue: false});
    private  Interest_Payment_Terms : ScenarioField = new ScenarioField({fieldValue: false});
    private  Interest_Rate : ScenarioField = new ScenarioField({fieldValue: false});
    private  International_Bank_Account_Identifier : ScenarioField = new ScenarioField({fieldValue: false});
    private  Investment_Account : ScenarioField = new ScenarioField({fieldValue: false});
    private  Investment_Bank : ScenarioField = new ScenarioField({fieldValue: false});
    private  Investment_Company : ScenarioField = new ScenarioField({fieldValue: false});
    private  Investment_Or_Deposit_Account : ScenarioField = new ScenarioField({fieldValue: false});
    private  Investment_Service : ScenarioField = new ScenarioField({fieldValue: false});
    private  Jurisdiction : ScenarioField = new ScenarioField({fieldValue: false});
    private  Legal_Agent : ScenarioField = new ScenarioField({fieldValue: false});
    private  Lender : ScenarioField = new ScenarioField({fieldValue: false});
    private  Loan_Or_Credit_Account : ScenarioField = new ScenarioField({fieldValue: false});
    private  Managed_Interest_Rate : ScenarioField = new ScenarioField({fieldValue: false});
    private  Payment_Service : ScenarioField = new ScenarioField({fieldValue: false});
    private  Policyholder : ScenarioField = new ScenarioField({fieldValue: false});
    private  Transaction_Type : ScenarioField = new ScenarioField({fieldValue: false});
    private  Transaction_Amount : ScenarioField = new ScenarioField({fieldValue: false});
    private  Transaction_ID : ScenarioField = new ScenarioField({fieldValue: false});
    private  Transaction_Mode : ScenarioField = new ScenarioField({fieldValue: false});
    private  Principal : ScenarioField = new ScenarioField({fieldValue: false});

    public constructor(init?:Partial<BankingScenario>) {
        Object.assign(this, init);
    }
}
