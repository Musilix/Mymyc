import { BankingScenario } from '../app/banking-scenario';
import { ScenarioField } from '../app/scenario-field';

export class BankingScenarioSource {
    private dormantTableRows = new Map<number, any>();
    private activatedTableRows = new Map<number, any>();

    // static for banking scenario data sources
    private BANKING_SCENARIO_DATA: BankingScenario[] = [
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Open a New Banking Account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Get Customer account details "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Get Customer Details "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize Account for 3rd Party Money Transfer "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Perform Transfer Funds Transaction "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Validate Customer Authentication "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " List account services "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Generate Account Statement "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Get Account History "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Open a New Basic Checking Account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Open a New Basic Savings Account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Open a New Deposit Account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Link Savings & Checking Account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a New Check book "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize a Deposit Transaction "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize a New payee for Making Bill Payment "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize a Utility service for making bill Payment "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize for Account to Account Money Transfer "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize for Wire Transfer "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorise for intra Bank Money transfer (Member to Meber) "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize for External Money transfer "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Link Savings & Checking with Investment Account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Transfer funds to Investment account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Receive funds from a Investment account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize an Investment account to link to savings account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize an Investment account to de-link to savings account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Add a New Contact number to Account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a Change of communication Mobile number "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Add a New Mailing -Billing address "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a change of Billing address "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request to udpate Billing Address "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a New loan account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Requeast for a New Loan disbursement "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a Loan detials "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for Loan amortization schedule "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a Loan fore closure "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a Loan re-payment "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a Loan statement "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request to issue  a Travellers cheque "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request to enroll for ACH payment to 3rd party "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request t stop ACH Payment "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Perform a Electronic Funds Transfer "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Perform a Electronic Check Deposit "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request to open a new additional service "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request to close an active account service "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Register a New Debit Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Generate a New Pin "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a New Debit Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for New Debit Card Pin "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize New Debit Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Activate New Debit Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " De-activate New Debot Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Get Active debit card Details "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Block Active Debit Card service "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Unblock Debit card service "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Change Debit Card Pin "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Get Debit Card Transaction Limit "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Get Debit Card Transaction Status "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Close a Debit Card Account "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for Debit Card Statement "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Register a New Credit Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Generate a New Pin "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for a New Credit Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Request for New Credit Card Pin "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize New Credit Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Activate New Credit Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " De-activate New Debot Card "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Get Active Credit card Details "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Block Active Credit Card service "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Unblock Credit card service "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Change Credit Card Pin "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Get Credit Card Transaction Limit "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Set New Credit Card Transaction Limit "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Set New Credit Card CASH Transaction Limit "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Set New Credit Card Shopping Transaction Limit "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Get Credit Card Transaction Status "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Suspend a Credit Card Transaction "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Issue-New Add-on Credit card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize New Add-on Credit card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Activate New Add-on Credit card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Generate a New Pin for Add-on Credit Card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Set Credit Limt for Add-on Credit Card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Set CASH transaction limit on Add-on Credit Card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Set Shopping Transaction limit on Add-on Credit Card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Suspend a Add-on Credit Card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Block Active Add-on Credit Card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Un Block Active Add-on Credit Card-1 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Issue-New Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Authorize New Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Activate New Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Generate a New Pin for Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Set Credit Limt for Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Set CASH transaction limit on Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Set Shopping Transaction limit on Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Suspend a Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Block Active Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Un Block Active Add-on Credit Card-2 "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Report a credit transaction as Un-Authorized "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Dispute a Credit Card transaction "})}),
        new BankingScenario({Scenario: new ScenarioField({fieldValue: " Close a Credit Card service Account "})})
    ];
    // Will there be any way to create these fields without the underscore?
    private bankingDefinedCols : string[] = ['Scenario', 'Account', 'Account_Holder', 'Account_Identifier', 'Account_Number', 'Account_Specific_Service_Agreement', 'Accounting_Transaction_Event', 'Accrual', 'Amortization', 'Amortization_Schedule', 'Bank', 'Bank_Account', 'Bank_Account_Identifier', 'Banking_Product', 'Banking_Service', 'Borrower', 'Borrowing_Capacity', 'Clearing_Bank', 'Collateral', 'Credit_Agreement', 'Date', 'Day_Count_Convention', 'Day_Of_Month', 'Fixed_Interest_Rate', 'Floating_Interest_Rate', 'Full_Amortization', 'Holding', 'Holding_Company', 'Insurance_Company', 'Insurance_Policy', 'Insurance_Service', 'Interest', 'Interest_Payment_Terms', 'Interest_Rate', 'International_Bank_Account_Identifier', 'Investment_Account', 'Investment_Bank', 'Investment_Company', 'Investment_Or_Deposit_Account', 'Investment_Service', 'Jurisdiction', 'Legal_Agent', 'Lender', 'Loan_Or_Credit_Account', 'Managed_Interest_Rate', 'Payment_Service', 'Payroll_Service', 'Policyholder', 'Principal', 'Principal_Repayment_Terms', 'Principal_Underwriter', 'Relationship_Manager', 'Relationship_Qualifier', 'Underwriter', 'Underwriting_Arrangement', 'Unilateral_Contract', 'Variable_Interest_Rate'];

    constructor(){
        let iterator = 0;
        this.BANKING_SCENARIO_DATA.forEach((bankingScenario: BankingScenario) => {
            this.dormantTableRows.set(iterator, bankingScenario);
            iterator++;
        });
    }

    setActiveRows(index, activatedScenario){
        this.activatedTableRows.set(index, activatedScenario);
    }

    getActiveRows(){
        return this.activatedTableRows;
    }

    getDormantRows(){
        return this.dormantTableRows;
    }

    getDataSource(){
        return this.BANKING_SCENARIO_DATA;
    }

    getDefinedCols(){
        return this.bankingDefinedCols;
    }
    printData(){
        console.log(this.BANKING_SCENARIO_DATA);
    }
}
