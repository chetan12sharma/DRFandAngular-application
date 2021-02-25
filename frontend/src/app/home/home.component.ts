import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { Plan } from '../models/plan';
import { AuthService } from '../service/auth.service';
import { MainService } from '../service/main.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private _mainservice: MainService, private sanitizer: DomSanitizer, private _route: Router, private _auth: AuthService) { }
  data: Plan[]
  htmlData: any
  ngOnInit(): void {

    this.fetchPlans()
  }

  showTrx = false
  private fetchPlans() {
    let obj = { 'user_id': sessionStorage.getItem('user_id') }
    this._mainservice.plan(obj).subscribe((response) => {
      this.data = response['data']

      console.log(this.data)
    }, (error) => {
      console.log(error)

    })
  }


  isSubscriptionExist() {
    for (const e of this.data) {
      if (e.sub__is_subscribed == true) {
        return true
      }
    }
  }

  activate(plan: Plan) {

    if (this.isSubscriptionExist()) {
      this._auth.openSnackBar(`User already have a subscribed plan acitvate.First unsubscribed activated plan`, 'cancel', 'red-snackbar')
    } else {
      console.log(plan)
      let obj = {
        'user_id': sessionStorage.getItem('user_id'),
        'amount': plan.plan_price
      }
      this.showTrx = true
      this._mainservice.activate(obj).subscribe((response) => {
        this.htmlData = response
        this.htmlData = this.sanitizer.bypassSecurityTrustHtml(this.htmlData)
        console.log(this.htmlData)
      }, (error) => {
        console.log(error)
      })

    }

  }

  cancelOrResumenPlan(plan: Plan) {
    let obj = {}
    obj["user_id"] = sessionStorage.getItem('user_id')
    this._mainservice.cancelOrResume(obj).subscribe((response) => {
      console.log(response)
      this.fetchPlans();
    }, (err) => {
      console.log(err)
    })
  }

  // 
  deactivate(plan: Plan) {
    let obj = {}
    obj["user_id"] = sessionStorage.getItem('user_id')
    this._mainservice.deactivate(obj).subscribe((response) => {
      console.log(response)
      this.fetchPlans();
    }, (err) => {
      console.log(err)
    })
  }

  logout() {
    sessionStorage.clear()
    this._route.navigate(['login'])
  }

}
