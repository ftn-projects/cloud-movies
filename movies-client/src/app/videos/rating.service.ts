import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environments} from "../../environments/evnironment";
import {Observable} from "rxjs";
import {AuthenticationService} from "../auth/authentication.service";

@Injectable({
  providedIn: 'root'
})
export class RatingService {

  constructor(private http: HttpClient,
              private authService: AuthenticationService) { }

  rateContent(contentId: string, rating: number): Observable<string> {
    const user: string = this.authService.getUserId();
    return this.http.post<string>(environments.api + `/ratings/${user}`, {rating: rating, contentId: contentId});
  }

}
