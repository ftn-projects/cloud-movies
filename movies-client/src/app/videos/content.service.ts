import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient, HttpParams} from "@angular/common/http";
import {environments} from "../../environments/evnironment";
import { Content } from "./models/content"
import {ContentDetails} from "./models/content-details";

@Injectable({
  providedIn: 'root'
})
export class ContentService {

  constructor(private http: HttpClient) { }

  getFeed(userId: string) {

  }

  getContentAdmin(): Observable<Content[]> {
    return this.http.get<Content[]>(environments.api + "/content");
  }

  getContentMetadata(contentId: string): Observable<ContentDetails> {
    return this.http.get<ContentDetails>(environments.api + `/content/${contentId}`);
  }
}
