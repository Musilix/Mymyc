import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ShareLoadingService {
  private isLoading : boolean = false;

  constructor() { }

  changeLoading(){
    this.isLoading = !this.isLoading;
  }

  checkLoading(){
    return this.isLoading;
  }
}
