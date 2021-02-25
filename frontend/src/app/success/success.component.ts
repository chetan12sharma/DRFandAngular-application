import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-success',
  templateUrl: './success.component.html',
  styleUrls: ['./success.component.css']
})
export class SuccessComponent implements OnInit {

  constructor(private _rotue: Router, private _activateRoute: ActivatedRoute,) { }
  orderid: string
  amount: any
  ngOnInit(): void {
    const routeParams = this._activateRoute.snapshot.paramMap;
    this.orderid = routeParams.get('orderId');
    this.amount = Number(routeParams.get('amount'))

    setTimeout(() => {
      this._rotue.navigate(['home'])
    }, 3000);
  }

}
