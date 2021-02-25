import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { User } from '../models/user';
@Injectable({
  providedIn: 'root'
})
export class MainService {

  constructor(private http: HttpClient) {

  }
  url = "http://127.0.0.1:8000/api/"

  login(obj: User) {
    return this.http.post(this.url + 'login', obj)
  }

  signup(obj: User) {
    console.log(User)
    return this.http.post(this.url + 'signup', obj)
  }

  plan(obj) {
    return this.http.post(this.url + 'plan', obj)
  }

  activate(obj) {
    return this.http.post(this.url + "activate", obj, { responseType: 'text' })
  }

  cancelOrResume(obj) {
    return this.http.post(this.url + "cancelOrResumePlan", obj)
  }

  deactivate(obj) {
    return this.http.post(this.url + "deactivate", obj)
  }


}