import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environments} from "../../environments/evnironment";
import { Content } from "./models/content"
@Injectable({
  providedIn: 'root'
})
export class VideoService {

  constructor(private http: HttpClient) { }

  getFeed(userId: string) {

  }

  getContentAdmin(): Observable<Content[]> {
    return this.http.get<Content[]>(environments.api + "/videos");
  }

  getContentMetadata(contentId: string) {

  }

  getStreamingLink(videoId: string) {
    // videoId should be ID from published bucket
    return this.http.get(environments.api + "/videos")
  }

  getDownloadLink(contentId: string) {

  }
}
