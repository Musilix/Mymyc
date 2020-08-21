import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import {PageEvent} from '@angular/material/paginator'
import { Scenario } from './scenario';
import { saveAs } from 'file-saver';

var iterator = 0;
var dormantTableRows = new Map<number, Scenario>();
var activatedTableRows = new Map<number, Scenario>();
const ELEMENT_DATA: Scenario[] = [
  new Scenario({Scenario:"Personal Auto", Gender:true}),
  new Scenario({Scenario: "New Business", Gender:true, DOB: true, Address: true}),
  new Scenario({Scenario: "Endorsement in the same new business"}),
  new Scenario({Scenario: "Renewal of an existing policy"}),
  new Scenario({Scenario: "Flat Cancellation"})
];

//initialize our dormant table with the scenarios... if one row is chosen, we use the id associated with it to put it in our activated table
ELEMENT_DATA.forEach((scenario: Scenario) => {
  dormantTableRows.set(iterator, scenario);
  iterator++;
});

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'mymic-frontend';

  constructor(private http: HttpClient){}


  definedColumns: string[] = ['Scenario', 'Gender', 'Address', 'DOB', 'firstName', 'lastName', 'Spouse_First_Name', 'Spouse_Last_Name', 'Spouse_DOB', 'Street_Address', 'Apt', 'City', 'County', 'Zip', 'State', 'Rent_or_Own', 'Email_Address', 'Primary_Phone', 'Secondary_Phone', 'Date_of_Purchase', 'Make', 'Model', 'Finance'];
  dataSource = ELEMENT_DATA;
  activeRows = activatedTableRows;

  // downloadTesting(){
  //   var FileSaver = require('file-saver');
  //   var blob = new Blob(["Hello, world!"], {type: "text/plain;charset=utf-8"});
  //   FileSaver.saveAs(blob, "hello world.txt");
  // }

  updateRowField(field, fieldVal, fieldLoc){
    let updatedFieldVal = !fieldVal;
    this.dataSource[fieldLoc][field] = updatedFieldVal;
  }

  testChange(index){
    if(activatedTableRows.get(index)){
      activatedTableRows.delete(index);
    }else{
      let activatedScenario = dormantTableRows.get(index)
      activatedTableRows.set(index, activatedScenario);
    }
  }

  testLink(rowData) {
    // console.log(data);
    // console.log(data[0]);
    // console.log(JSON.parse(rowData));
    // console.log(JSON.stringify(data));

    this.http.post<any>('http://127.0.0.1:5000/api/test-send', { rows: JSON.parse(rowData)}).subscribe(data => {
      console.log("Sending data to server...");
      console.log("Waiting for response... ");
      console.log("Returned:" + data);
    })
  }

  requestData(){
    // console.log(this.mapToJson(activatedTableRows));
    this.testLink(this.mapToJson(activatedTableRows));
  }

  mapToJson(map){
    return JSON.stringify(Array.from(map.entries()));
  }

}
