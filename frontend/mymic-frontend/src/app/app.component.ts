import { Component } from '@angular/core';
import { MatTabChangeEvent } from '@angular/material/tabs';
import { HttpClient } from '@angular/common/http';

import { ShareLoadingService } from '../app/share-loading.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'mymic-frontend';

  isLoading : boolean;

  toggle : boolean = false;

  isHealthcare : boolean = false;
  isInsurance : boolean = false;
  isBanking : boolean = false;

  constructor(private http : HttpClient, private loadingService : ShareLoadingService){
    this.isLoading = loadingService.isLoading;
  }

  handleToggle(event ?: MatTabChangeEvent){
    if(event){
      let toggledTab = event.tab.textLabel
      if(toggledTab != "Generate"){
        this.toggleHelp();
      }
    }else{
      this.toggleHelp();
    }
  }

  toggleHelp(){
    if(!this.toggle){
      this.toggle = true;
    }
  }

  changeDomain(domainIndex){
    if(domainIndex === 0){
      // console.log("Home");
      this.isHealthcare = false;
      this.isInsurance = false;
      this.isBanking = true;
    }else if(domainIndex === 1){
      this.isHealthcare = true;
      this.isInsurance = false;
      this.isBanking = false;
    }else if(domainIndex === 2){
      this.isHealthcare = false;
      this.isInsurance = true;
      this.isBanking = false;
    }
  }

  ngOnInit(){
  }
}
