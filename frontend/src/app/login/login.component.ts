import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { User } from "../models/user";
import { MainService } from '../service/main.service';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private route: Router, private mainservice: MainService, private _snakebar: MatSnackBar) { }
  ngOnInit(): void {
    sessionStorage.clear()
  }

  model = new User();

  onSubmit(form: NgForm) {
    this.mainservice.login(form.value).subscribe((result) => {
      console.log(result)
      sessionStorage.setItem("token", result['access'])
      sessionStorage.setItem("first_name", result['first_name'])
      sessionStorage.setItem("user_id", result['id'])
      this.route.navigate(['home'])

    }, (err) => {
      form.resetForm()
    })
  }
}
