import { Component } from '@angular/core';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'mymic-frontend';

  isHome = false;
  isAuto = false;
  isLife = false;

  changeDomain(domainIndex){
    console.log("domain chosen");
    console.log("domain index: " + domainIndex);
    console.log("domain index type: " + typeof domainIndex);
    console.log("-----------");
    
    if(domainIndex === 0){
      // console.log("Home");
      this.isHome = false;
      this.isAuto = false;
      this.isLife = true;
    }else if(domainIndex === 1){
      this.isHome = true;
      this.isAuto = false;
      this.isLife = false;
    }else if(domainIndex === 2){
      this.isHome = false;
      this.isAuto = true;
      this.isLife = false;
    }
  }
}
