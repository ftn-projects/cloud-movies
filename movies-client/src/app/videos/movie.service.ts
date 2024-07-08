import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {environments} from "../../environments/evnironment";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  constructor(private http: HttpClient) { }


  getStreamingLinkMovie(videoId:string, resolution: string): Observable<string> {
    return this.http.get<string>(environments.api + `/video/${videoId}/${resolution}`);
  }

  deleteMovie(movieId: string): Observable<void> {
    return this.http.delete<void>(environments.api + `/movie/${movieId}`);
  }
}
