import { Component, OnInit, ViewChild, Input, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// import { Scenario } from '.././scenario';
import { BankingScenarioSource } from '../banking-scenario-source';
import { BankingScenario } from '../banking-scenario';

import { HealthcareScenario } from '../healthcare-scenario';
import { HealthcareScenarioSource } from '../healthcare-scenario-source';

import { InsuranceScenario } from '../insurance-scenario';
import { InsuranceScenarioSource } from '../insurance-scenario-source';

import { ScenarioField } from '.././scenario-field';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource} from '@angular/material/table';
import { ScenarioDomain } from '../ScenarioDomain.enum';

import { ScenarioSource } from '../scenario-source';

import { ShareLoadingService } from '../share-loading.service';

@Component({
  selector: 'app-scenario-table',
  templateUrl: './scenario-table.component.html',
  styleUrls: ['./scenario-table.component.css']
})
export class ScenarioTableComponent implements OnInit {

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef, private loadingService : ShareLoadingService){}

  // find better way to keep track of the varying data options - insurance, health, banking
  // static for banking scenario data sources
  private BANKING_SCENARIO_DATA : BankingScenario[] = [
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Open a New Banking Account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Get Customer account details"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Get Customer Details"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize Account for 3rd Party Money Transfer"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Perform Transfer Funds Transaction"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Validate Customer Authentication"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "List account services"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Generate Account Statement"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Get Account History"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Open a New Basic Checking Account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Open a New Basic Savings Account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Open a New Deposit Account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Link Savings & Checking Account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a New Check book"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize a Deposit Transaction"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize a New payee for Making Bill Payment"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize a Utility service for making bill Payment"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize for Account to Account Money Transfer"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize for Wire Transfer"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorise for intra Bank Money transfer (Member to Meber)"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize for External Money transfer"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Link Savings & Checking with Investment Account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Transfer funds to Investment account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Receive funds from a Investment account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize an Investment account to link to savings account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize an Investment account to de-link to savings account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Add a New Contact number to Account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a Change of communication Mobile number"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Add a New Mailing/Billing address"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a change of Billing address"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request to update Billing Address"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a New loan account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Requeast for a New Loan disbursement"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a Loan detials"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for Loan amortization schedule"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a Loan fore closure"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a Loan re-payment"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a Loan statement"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request to issue  a Travellers cheque"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request to enroll for ACH payment to 3rd party"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request t stop ACH Payment"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Perform a Electronic Funds Transfer"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Perform a Electronic Check Deposit"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request to open a new additional service"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request to close an active account service"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Register a New Debit Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Generate a New Pin"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a New Debit Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for New Debit Card Pin"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize New Debit Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Activate New Debit Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "De-activate New Debot Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Get Active debit card Details"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Block Active Debit Card service"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Unblock Debit card service"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Change Debit Card Pin"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Get Debit Card Transaction Limit"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Get Debit Card Transaction Status"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Close a Debit Card Account"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for Debit Card Statement"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Register a New Credit Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Generate a New Pin"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for a New Credit Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Request for New Credit Card Pin"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize New Credit Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Activate New Credit Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "De-activate New Debot Card"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Get Active Credit card Details"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Block Active Credit Card service"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Unblock Credit card service"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Change Credit Card Pin"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Get Credit Card Transaction Limit"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Set New Credit Card Transaction Limit"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Set New Credit Card CASH Transaction Limit"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Set New Credit Card Shopping Transaction Limit"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Get Credit Card Transaction Status"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Suspend a Credit Card Transaction"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Issue-New Add-on Credit card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize New Add-on Credit card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Activate New Add-on Credit card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Generate a New Pin for Add-on Credit Card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Set Credit Limt for Add-on Credit Card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Set CASH transaction limit on Add-on Credit Card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Set Shopping Transaction limit on Add-on Credit Card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Suspend a Add-on Credit Card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Block Active Add-on Credit Card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Un Block Active Add-on Credit Card-1"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Issue-New Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Authorize New Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Activate New Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Generate a New Pin for Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Set Credit Limt for Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Set CASH transaction limit on Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Set Shopping Transaction limit on Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Suspend a Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Block Active Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Un Block Active Add-on Credit Card-2"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Report a credit transaction as Un-Authorized"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Dispute a Credit Card transaction"})}),
      new BankingScenario({Scenario: new ScenarioField({fieldValue: "Close a Credit Card service Account"})})
  ];
  // Will there be any way to create these fields without the underscore?
  private bankingDefinedCols : string[] = ['Scenario', 'Account', 'Account_Holder', 'Account_Identifier', 'Account_Number', 'Bank_Routing_Number', 'Account_Balance', 'Account_Specific_Service_Agreement', 'Accrual', 'Amortization', 'Amortization_Schedule', 'Bank', 'Bank_Account', 'Bank_Account_Identifier', 'Banking_Product', 'Banking_Service', 'Borrower', 'Borrowing_Capacity', 'Clearing_Bank', 'Collateral', 'Credit_Agreement', 'Credit_Card_Number', 'Credit_Card_Type', 'Credit_Card_Expiry', 'Credit_Card_Cvv', 'Check_Number', 'Check_Dated', 'Check_Deposited_Date', 'Check_Deposit_Type', 'Check_Type', 'MICR_Code', 'Date', 'Time_Stamp', 'Debit_Card_Number', 'Debit_Card_Type', 'Debit_Card_Expiry', 'Debit_Card_Cvv', 'Fixed_Interest_Rate', 'Floating_Interest_Rate', 'Full_Amortization', 'Holding', 'Holding_Company', 'Insurance_Company', 'Insurance_Policy', 'Insurance_Service', 'Interest', 'Interest_Payment_Terms', 'Interest_Rate', 'International_Bank_Account_Identifier', 'Investment_Account', 'Investment_Bank', 'Investment_Company', 'Investment_Or_Deposit_Account', 'Investment_Service', 'Jurisdiction', 'Legal_Agent', 'Lender', 'Loan_Or_Credit_Account', 'Managed_Interest_Rate', 'Payment_Service', 'Policyholder', 'Transaction_Type', 'Transaction_Amount', 'Transaction_ID', 'Transaction_Mode', 'Principal']
  private HEALTHCARE_SCENARIO_DATA : HealthcareScenario[] = [
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Enroll a Behavioral practictioner"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Edit Behavioral practictioner enrollment"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Enroll a Medical practitioner"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Edit Medical practitioner enrollment"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Enroll a Dental provider"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Edit  Dental provider enrollment"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Enroll an Independent broker"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Enroll broker who is registered with an agency"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "For active brokers calculate the commission"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Submit claims for a member -non accident/non hospital admission case"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Edit claims data for a member -non accident/non hospital admission case"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Check submitted claim status for a member -non accident/non hospital admission case"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Enroll/re-enroll a member - with no dependants"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Reinstate a member - with no dependants"})}),
    new HealthcareScenario({Scenario: new ScenarioField({fieldValue: "Remove a member - with no dependants"})})
  ];

  private healthcareDefinedCols : string[] = ['Scenario', 'First_Name', 'Last_Name', 'DOB', 'Gender', 'SSN', 'Email_Address', 'Phone_Number', 'Street_Address', 'State', 'Zip', 'License_Issue_State', 'License_Issue_Date', 'License_Expiry_Date', 'License_Number', 'Agency_Name', 'Employer_Name', 'Employment_Status', 'Speciality_Behavioral', 'Applying_As', 'Broker_Number', 'Pay_Commissions_To', 'CAQH_Provider_ID', 'Hospital_Affiliation_State', 'NPI_Number', 'Population_Worked_With', 'Medicare_Certified_State', 'PTAN_Number', 'Speciality_Medical', 'Participating_Association', 'Speciality_Dental', 'Policy_ID', 'Date_First_Consulted', 'Physician_Name', 'Illness', 'Claim_Submission_Date', 'CPT_Code', 'Broker_Status', 'Broker_Bonus', 'Broker_Commission', 'Claim_ID', 'Total_Bill', 'Hospital_ID', 'Claim_Process_Date', 'Claim_Status', 'Plan_Type', 'Benefits', 'Effective_Date', 'Amount_To_HSA']
  private INSURANCE_SCENARIO_DATA : InsuranceScenario[] = [
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "New Business"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "Endorsement"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "Renewal"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "Cancellation"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "Reinstatement"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "Rewrite"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "Out Of Sequence Transaction"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "Midterm Endorsement"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "OOS Endorsement Converted Renewal"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "Pro-Rate Endorsement For Adding A Vehicle"})}),
    new InsuranceScenario({Scenario: new ScenarioField({fieldValue: "Pro-Rate Endorsement Deleting A Vehicle"})})
  ];
  private insuranceDefinedCols : string[] = ['Scenario', 'Policy_Number', 'Insured_First_Name', 'Insured_Middle_Name', 'Insured_Last_Name', 'Date_Of_Birth', 'Gender', 'Maritial_Status', 'Spouse_First_Name', 'Spouse_Last_Name', 'Spouse_Dob', 'State', 'City', 'County', 'Street_Address', 'Apt', 'Zip_Code', 'Email_Address', 'Primary_Phone', 'Secondary_Phone', 'Date_Of_Purchase', 'Make', 'Model', 'Vin_Number', 'Finance', 'Primary_Usage', 'Ride_Sharing_Program', 'Garage_Address', 'Miles_Driven_Per_Day', 'Days_Driven_In_A_Week', 'Total_Miles_Per_Year', 'Safety_Device', 'Employment_Status', 'Age_While_Taking_License', 'Accident_Or_Violation_In_Past_5_Years', 'Spouse_Employment_Status', 'Spouse_Age_While_Taking_License', 'Primary_Driver', 'Secondary_Driver', 'Bodily_Injured_Liability_Coverage', 'Bodily_Injured_Per_Person', 'Bil_Per_Occurance', 'Property_Damage_Liability_Coverage', 'Property_Damage_Limit_Per_Occurance', 'Collision_Coverage', 'Collision_Deductible', 'Comprehensive_Coverage', 'Comprehensive_Deductible', 'Rental_Reimbursement', 'Rental_Reimbursement_Limit'];

  @Input()
  domain : string;
  amtOfData : number = 1; //implicitly generate 1 data by default

  // change type to general Scenario type, which each domain class implments - with general methods like get, set, etc...
  scenarioDataSource : ScenarioSource; 
  definedColumns : string[];
  activeRows : Map<number, any>;
  dataSource : MatTableDataSource<any> = new MatTableDataSource();
  @ViewChild(MatPaginator) paginator : MatPaginator;

  activateRow(index){
    let activatedTableRows = this.scenarioDataSource.getActiveRows();
    let dormantTableRows = this.scenarioDataSource.getDormantRows();
    if(activatedTableRows.get(index)){
      activatedTableRows.delete(index);
    }else{
      let activatedScenario = dormantTableRows.get(index)
      this.scenarioDataSource.setActiveRows(index, activatedScenario);
      // activatedTableRows.set(index, activatedScenario);
    }
  }

  requestData(){
    let activatedTableRows = this.scenarioDataSource.getActiveRows();
    this.sendData(this.mapToJson(activatedTableRows), this.amtOfData);
  }

  sendData(rowData, amt) {
    let requestOptions = {
      responseType: "blob"
    };
    // const headers = new HttpHeaders().set('Content-Type', 'text/csv; charset=utf-8');

    console.log("Sending data to server...");

    this.loadingService.nextLoadMessage(true);

    //jesus fucking christ... all this time I had to set the responseType to blob... or arraybuffer! It was opting to JSON
    //and in turn having many parsin errors from the stuff i was sending back from the Flask server... jeez, good to know for the future.
    this.http.post('http://127.0.0.1:5000/api/test-send', { rows: JSON.parse(rowData), amt: amt}, { responseType: 'blob', observe: 'response'}).subscribe(response => {
      let fileName = response.headers.get('Content-Disposition');
      let x = response.headers.get("Type-Stream")

      if (x == "zip"){
        this.downLoadFile(response.body,"Scenarios", "application/zip", "zip");
      }else{
        this.downLoadFile(response.body, fileName, "text/csv", "csv")
      }
      this.loadingService.nextLoadMessage(false);
    })
  }

  downLoadFile(data: any, fileName: string, type: string, extension : string) {
    let blob = new Blob([data], { type: type });

    let a = window.document.createElement("a");
    a.href = window.URL.createObjectURL(blob);
    if(extension === "csv"){
      a.download = fileName + ".csv";
    }else if(extension === "zip"){
      a.download = fileName + ".zip";
    }

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  mapToJson(map){
    return JSON.stringify(Array.from(map.entries()));
  }

  ngOnInit(): void {
    if(this.domain == "Banking"){
      this.scenarioDataSource = new BankingScenarioSource(this.BANKING_SCENARIO_DATA, this.bankingDefinedCols);
    }else if(this.domain == "Healthcare"){
      this.scenarioDataSource = new HealthcareScenarioSource(this.HEALTHCARE_SCENARIO_DATA, this.healthcareDefinedCols);
    }else if(this.domain == "Insurance"){
      this.scenarioDataSource = new InsuranceScenarioSource(this.INSURANCE_SCENARIO_DATA, this.insuranceDefinedCols);
    }
  }

  // whoa! this worked now?! It didnt before... maybe because I didnt have that viewChild paginator value connected to
  // the mattabledatasource value? Idk... but this works now!
  ngAfterViewInit(){
    this.dataSource.paginator = this.paginator
    this.dataSource.data = this.scenarioDataSource.getDataSource();
 
    this.activeRows = this.scenarioDataSource.getActiveRows();
    this.definedColumns = this.scenarioDataSource.getDefinedCols();

    this.cdr.detectChanges();
  }
}
