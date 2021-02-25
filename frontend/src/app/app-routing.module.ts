import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FailedComponent } from './failed/failed.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { SuccessComponent } from './success/success.component';
import {
  AuthGuardService as AuthGuard
} from './service/authgaurd.service';
const routes: Routes = [
  { path: "", redirectTo: "login", pathMatch: "full" },
  { path: "login", component: LoginComponent },
  { path: "register", component: RegisterComponent },
  { path: "home", component: HomeComponent, canActivate: [AuthGuard] },
  { path: "success/:orderId/:amount", component: SuccessComponent },
  { path: "fail/:orderId/:amount", component: FailedComponent },
  { path: '**', redirectTo: 'login' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
