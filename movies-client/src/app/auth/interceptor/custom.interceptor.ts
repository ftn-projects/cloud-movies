import {HttpEvent, HttpHandler, HttpInterceptor, HttpInterceptorFn, HttpRequest} from '@angular/common/http';
import {Router} from "@angular/router";
import {AuthenticationService} from "../authentication.service";
import {mergeMap, Observable} from "rxjs";

export class CustomInterceptor implements HttpInterceptor {

  constructor(private router: Router,
              private authService: AuthenticationService) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return this.authService.getAccessToken()?.pipe(
      mergeMap((token) => {
        req = req.clone(
          {
            headers: req.headers.set('Authorization', `Bearer ${token}`)
          }
        )
        return next.handle(req);
      })
    )



  }
};
