import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ShareLoadingService {
  private internalLoadingCheck = new BehaviorSubject(false);
  isLoading : Observable<boolean> = this.internalLoadingCheck.asObservable();

  constructor() { }

  nextLoadMessage(state : boolean){
    this.internalLoadingCheck.next(state);
  }
}
