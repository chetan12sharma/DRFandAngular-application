import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-failed',
  templateUrl: './failed.component.html',
  styleUrls: ['./failed.component.css']
})
export class FailedComponent implements OnInit {

  constructor(private _rotue: Router, private _activateRoute: ActivatedRoute,) { }
  orderid: string
  amount: Number
  ngOnInit(): void {
    const routeParams = this._activateRoute.snapshot.paramMap;
    this.orderid = routeParams.get('orderId');
    this.amount = Number(routeParams.get('amount'))
    setTimeout(() => {
      this._rotue.navigate(['home'])
    }, 3000);
  }

}
