import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { AuthService } from './auth.service';
@Injectable({
    providedIn: 'root'
})
export class AuthGuardService implements CanActivate {
    constructor(public _auth: AuthService, public router: Router) { }

    canActivate(): boolean {
        if (!this._auth.isAuthenticated()) {
            this.router.navigate(['login']);
            return false;
        }
        return true;
    }
}