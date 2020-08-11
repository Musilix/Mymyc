import { Component } from '@angular/core';
import {PageEvent} from '@angular/material/paginator'

//current awful way of keeping track of fields which are required... just have an array containing val of checkbox, as well as if it required or not... eh
export interface PeriodicElement {
  scenario: string;
  gender: [boolean, boolean];
  address: [boolean, boolean];
  firstName: [boolean, boolean];
  lastName: [boolean, boolean];
}


export interface Scenario{
  Scenario_Description: string,
  Policy_Number_Mandatory : number;
  Insured_First_Name : string;
  Insured_Middle_Name : string;
  Insured_Last_Name : string;
  DOB : Date;
  Gender : string;
  Maritial_Status : string;
  Spouse_First_Name : string;
  Spouse_Last_Name : string;
  Spouse_DOB : Date;
  Street_Address : string;
  Apt : string;
  City : string;
  County : string;
  Zip : number;
  State : string;
  Rent_or_Own : string;
  Email_Address : string;
  Primary_Phone : string;
  Secondary_Phone : string;
  Date_of_Purchase : string;
  Make : string;
  Model : string;
  Finance : string;
  Primary_Usage : string;
  Ride_Sharing_Program : string;
  Garage_Address : string;
  Miles_driven_per_day : number;
  Days_driven_in_a_week : number;
  Total_miles_per_year : number;
  safety_device : string;
  Employment_Status : string;
  Age_while_taking_license : number;
  Accident_n_violation_in_past_5_yrs : number;
  Spouse_employment_status : string;
  Spouse_age_while_taking_license : string;
  Primary_Driver : string;
  Secondary_Driver : string;
  Bodily_Injured_Liability : string;
  BIL_Per_person : string;
  BIL_Per_accident : string;
  PD_Liability : string;
  Collision : string;
  Comprehensive : string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {scenario: 'Personal Auto', gender: [false, false], address: [true, true], firstName:[false, false], lastName: [false, false]},
  {scenario: 'New Business', gender: [false, false], address: [false, false], firstName:[false, false], lastName: [false, false]},
  {scenario: 'Endorsement in the same new business', gender: [false, false], address: [false, false], firstName:[false, false], lastName: [false, false]},
  {scenario: 'Renewal of an existing policy', gender: [true, true], address: [true, true], firstName:[true, true], lastName: [true, true]},
  {scenario: 'Flat Cancellation', gender: [false, false], address: [true, true], firstName:[false, false], lastName: [false, false]}
];


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'mymic-frontend';
 
  displayedColumns: string[] = ['scenario', 'gender', 'address', 'first name', 'last name'];
  dataSource = ELEMENT_DATA;

  // column_headers: string[] = ["Policy Number - Mandatory", "Insured First Name", "Insured Middle Name", "Insured Last Name", "DOB", "Gender", "Maritial Status", "Spouse First Name", "Spouse Last Name", "Spouse DOB", "Street Address", "Apt", "City", "County", "Zip", "State",	"Rent or Own", "E-mail Address",	"Primary Phone", "Secondary Phone", "Date of Purchase", "Make", "Model", "Finance", "Primary Usage", "Ride Sharing Program", "Garage Address", "Miles driven/day", "Days driven in a week", "Total miles per year", "safety device", "Employment Status", "Age while taking license", "Accident/violation in past 5 yrs",	"Spouse employment status", "Spouse age while taking license", "Primary Driver", "Secondary Driver", "Bodily Injured Liability", 	"BIL Per person", "BIL Per accident", "PD Liability", "Collision", 	"Comprehensive"]; 
  SCENARIO_DATA: string[] = [
    'Personal Auto',
    'New Business',
    'Endorsement in the same new business',
    'Renewal of an existing policy',
    'Flat Cancellation'
 ];
}
