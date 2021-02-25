import { Injectable } from '@angular/core';
import {
    HttpRequest,
    HttpHandler,
    HttpEvent,
    HttpInterceptor,
    HttpResponse,
    HttpErrorResponse
} from '@angular/common/http';

import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';

@Injectable()
export class HttpConfigInterceptor implements HttpInterceptor {
    constructor(private _auth: AuthService, private _route: Router) { }
    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

        if (sessionStorage.length != 0) {
            const token = sessionStorage.getItem("token")
            request = request.clone({
                setHeaders: {
                    Authorization: `Bearer ${token}`
                }
            });
        }
        return next.handle(request).pipe(
            catchError((error: HttpErrorResponse) => {
                let data = {};
                debugger;
                data = {
                    reason: error && error.error ? error.error.detail || error.error.email : 'Error occur',
                    status: error.status
                };
                this._auth.openSnackBar(data['reason'], 'close',
                    'red-snackbar');

                if (error.error.code == "token_not_valid") {
                    this._route.navigate(['login'])
                }
                return throwError(error);
            }));
    }
}