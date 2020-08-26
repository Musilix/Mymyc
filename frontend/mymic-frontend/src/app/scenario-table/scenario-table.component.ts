import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders  } from '@angular/common/http';
import { Scenario } from '.././scenario';
import { ScenarioField } from '.././scenario-field';

var iterator = 0;
var dormantTableRows = new Map<number, Scenario>();
var activatedTableRows = new Map<number, Scenario>();
const ELEMENT_DATA: Scenario[] = [
  new Scenario({Scenario: new ScenarioField({fieldValue: "Personal Auto"}), Gender:new ScenarioField({fieldValue: true, required:true})}),
  new Scenario({Scenario: new ScenarioField({fieldValue: "New Business"}), Gender:new ScenarioField({fieldValue: true, required:true}), DOB: new ScenarioField({fieldValue: true, required: true}), Address: new ScenarioField({fieldValue: true, required: true})}),
  new Scenario({Scenario: new ScenarioField({fieldValue: "Endorsement in the same new business"})}),
  new Scenario({Scenario: new ScenarioField({fieldValue: "Renewal of an existing policy"})}),
  new Scenario({Scenario: new ScenarioField({fieldValue: "Flat Cancellation"})})
];

//initialize our dormant table with the scenarios... if one row is chosen, we use the id associated with it to put it in our activated table
ELEMENT_DATA.forEach((scenario: Scenario) => {
  dormantTableRows.set(iterator, scenario);
  iterator++;
});

@Component({
  selector: 'app-scenario-table',
  templateUrl: './scenario-table.component.html',
  styleUrls: ['./scenario-table.component.css']
})
export class ScenarioTableComponent implements OnInit {

  
  constructor(private http: HttpClient){}


  amtOfData = 1; //implicitly generate 1 data by default
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

  testLink(rowData, amt) {
    let requestOptions = {
      responseType: "blob"
    };
    // const headers = new HttpHeaders().set('Content-Type', 'text/csv; charset=utf-8');

    //jesus fucking christ... all this time I had to set the responseType to blob... or arraybuffer! It was opting to JSON
    //and in turn having many parsin errors from the stuff i was sending back from the Flask server... jeez, good to know for the future.
    this.http.post('http://127.0.0.1:5000/api/test-send', { rows: JSON.parse(rowData), amt: amt}, { responseType: 'arraybuffer' }).subscribe(response => {
      this.downLoadFile(response, "text/csv")
      console.log("Sending data to server...");
    })
  }

  downLoadFile(data: any, type: string) {
    let blob = new Blob([data], { type: type });

    let a = window.document.createElement("a");
    a.href = window.URL.createObjectURL(blob);
    a.download = "test.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  requestData(){
    console.log("Requested rows: " + this.amtOfData);

    this.testLink(this.mapToJson(activatedTableRows), this.amtOfData);
  }

  mapToJson(map){
    return JSON.stringify(Array.from(map.entries()));
  }

  ngOnInit(): void {
  }

}
