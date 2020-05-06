import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class StateService {
  private currentPostList: any[] = [];
  constructor() { }

  getCurrentPostList() {
    return this.currentPostList;
  }

  setCurrentPostList(currentPostList: any[]) {
    this.currentPostList = currentPostList;
  }
}
