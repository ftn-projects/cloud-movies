import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {environments} from "../../environments/evnironment";
import {Episode} from "./models/episode";
import {HttpClient, HttpParams} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ShowService {

  constructor(private http: HttpClient) { }


  getSeasons(videoId: string): Observable<string[]> {
    return this.http.get<string[]>(environments.api + `/show/${videoId}/season`)
  }
  getSeasonEpisodes(videoId:string, season: string): Observable<Episode[]> {
    return this.http.get<Episode[]>(environments.api + `/show/${videoId}/season/${season}`);
  }

  getStreamingLinkTvShow(videoId: string, resolution: string, season: string, episode: string): Observable<string> {
    let params: HttpParams = new HttpParams();
    params.set('season', season);
    params.set('episode', episode);
    return this.http.get<string>(environments.api + `/video/${videoId}/${resolution}`, {params: params});
  }

  getSeasonsWithEpisodes(showId: string): Observable<any> {
    return this.http.get<any>(environments.api + `/show/${showId}/seasonDetails`);
  }
}
