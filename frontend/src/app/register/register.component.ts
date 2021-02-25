import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { User } from "../models/user";
import { MainService } from '../service/main.service';
import * as moment from 'moment';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  constructor(private route: Router, private _mainservice: MainService) { }

  ngOnInit(): void {
  }

  model = new User();
  minDate = "0001-01-01"
  maxDate = moment(new Date()).format('YYYY-MM-DD')
  onSubmit(form: NgForm) {
    console.log(form.value)

    this._mainservice.signup(form.value).subscribe((response) => {
      console.log(response)
      this.route.navigate(['login'])
    }, (error) => {
      form.resetForm()
    })

  }

}
