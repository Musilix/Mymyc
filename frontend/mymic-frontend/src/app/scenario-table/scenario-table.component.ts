import { Component, OnInit, ViewChild, Input, ChangeDetectorRef } from '@angular/core';
import { HttpClient, HttpHeaders  } from '@angular/common/http';
// import { Scenario } from '.././scenario';
import { BankingScenarioSource } from '../banking-scenario-source';
import { BankingScenario } from '../banking-scenario';
import { ScenarioField } from '.././scenario-field';
import { MatPaginatorModule, MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource} from '@angular/material/table';

@Component({
  selector: 'app-scenario-table',
  templateUrl: './scenario-table.component.html',
  styleUrls: ['./scenario-table.component.css']
})
export class ScenarioTableComponent implements OnInit {

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef){}

  @Input()
  domain : string;
  amtOfData : number = 1; //implicitly generate 1 data by default

  // change type to general Scenario type, which each domain class implments - with general methods like get, set, etc...
  scenarioDataSource; //change this to check domain and use proper domain class obj
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
      console.log("Sending data to server...");
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
    // console.log(this.domain == "Banking");
    this.scenarioDataSource = (this.domain == "Banking") ? new BankingScenarioSource() : null;
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
