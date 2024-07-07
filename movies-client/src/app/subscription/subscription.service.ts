import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {UserSubs} from "./model/user-subs";
import {environments} from "../../environments/evnironment";
import {AuthenticationService} from "../auth/authentication.service";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {

  constructor(private http: HttpClient,
              private authService: AuthenticationService) { }

  subscribe(type: string,  name: string): Observable<string> {
    const body = {type: type, name:name}
    const userId: string = this.authService.getUserId();
    console.log(userId);
    return this.http.post<string>(environments.api + `/subscription/${userId}`, body);
  }

  unsubscribe(type: string, name: string): Observable<string> {
    const userId = this.authService.getUserId();
    return this.http.delete<string>(environments.api + `/subscription/${userId}/${type}/${name}`);
  }

  getSubscriptions(): Observable<UserSubs>{
    const userId: string = this.authService.getUserId();
    return this.http.get<UserSubs>(environments.api + `/subscription/${userId}`);
  }

}
