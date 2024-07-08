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

  createShow(details: any): Observable<string> {
    return this.http.post<string>(environments.api + `/show`, details);
  }

  deleteShow(showId: string): Observable<void> {
    return this.http.delete<void>(environments.api + `/show/${showId}`);
  }

  addSeason(showId: string, title: any, releaseDate: any): Observable<any> {
    return this.http.post(environments.api + `/show/${showId}`, {title, releaseDate});
  }

  deleteSeason(showId: string, season: any): Observable<void> {
    return this.http.delete<void>(environments.api + `/show/${showId}/${season}`);
  }

  swapSeasons(showId: string, first: number, second: number): Observable<void> {
    return this.http.put<void>(environments.api + `/show/${showId}/swapSeason`, {first, second});
  }

  swapEpisodes(showId: string, season: number, first: number, second: number): Observable<void> {
    return this.http.put<void>(environments.api + `/show/${showId}/${season}/swapEpisode`, {first, second});
  }

  deleteEpisode(showId: string, season: number, episode: number): Observable<void>{
    return this.http.delete<void>(environments.api + `/show/${showId}/${season}/${episode}`);
  }

  saveEpisodeDetails(showId: string, season: number, episode: number, details: any): Observable<any> {
    return this.http.put(environments.api + `/show/${showId}/${season}/${episode}`, details);
  }

  getEpisodeDetails(showId: string, season: number, episode: number): Observable<any> {
    return this.http.get<any>(environments.api + `/show/${showId}/${season}/${episode}`);
  }
}
