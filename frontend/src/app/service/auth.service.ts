import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { MatSnackBar } from '@angular/material/snack-bar';
@Injectable({
    providedIn: 'root'
})
export class AuthService {

    constructor(private http: HttpClient, private _snackBar: MatSnackBar) {

    }

    openSnackBar(message: string, action: string, className: string) {
        this._snackBar.open(message, action, {
            duration: 2000,
            verticalPosition: 'top',
            horizontalPosition: 'end',
            panelClass: [className],
        });
    }

    result: boolean = false
    isAuthenticated(): boolean {
        const token = sessionStorage.getItem('token');
        if (token != null) {
            return true
        }
        return false
    }
}