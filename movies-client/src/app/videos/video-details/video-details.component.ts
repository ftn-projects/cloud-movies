import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {ContentService} from "../content.service";
import {MatSelectChange} from "@angular/material/select";
import {AuthenticationService} from "../../auth/authentication.service";
import {ContentDetails} from "../models/content-details";
import {Episode} from "../models/episode";
import {RatingService} from "../rating.service";
import {SubscriptionService} from "../../subscription/subscription.service";
import {ShowService} from "../show.service";
import {MovieService} from "../movie.service";

@Component({
  selector: 'app-video-details',
  templateUrl: './video-details.component.html',
  styleUrl: './video-details.component.css'
})
export class VideoDetailsComponent implements OnInit {
  videoId: string = '';
  videoSource: string = '';
  userRole: string = '';

  seasons: string[] = ['Select season'];
  selectedSeason: string | undefined = '';

  selectedEpisode: Episode | undefined = {episodeNumber:0, title: '', description:'', duration:''};
  episodesOfSeason: Episode[] = [{episodeNumber:1, title:'Pilot', description:'Some episode desc', duration:'90'}];

  contentDetails: ContentDetails = {
    videoId: '',
    videoType: '',
    title: 'Some title goes here',
    actors: ['Pera Peric', 'Neko Drugi', 'Neko Treci'],
    directors: ['Misa Misic', 'Zdera Zderic'],
    releaseDate: '',
    description: 'Some desc goes here and it describes movie/content/tvoshow',
    duration: '',
    genres: ['Horror', 'Comedy', 'Action'],
  }

  constructor(private route: ActivatedRoute,
              private contentService: ContentService,
              private showService: ShowService,
              private authService: AuthenticationService,
              private movieService: MovieService,
              private subService: SubscriptionService,
              private ratingService: RatingService) {
  }

  ngOnInit(): void {
    // get content data then decide if needed other info
    this.route.paramMap.subscribe(params => {
      this.videoId = params.get('videoId') || '';
    });
    // fetch the meta data, get id-s for video in different resolutions
    this.authService.userRoleState.subscribe((role) => {
      this.userRole = role;
    });
    this.authService.getUserRole();

    this.contentService.getContentMetadata(this.videoId).subscribe({
      next: data => {
        this.contentDetails = data;
        if (this.contentDetails.videoType === 'TV-SHOW') {
          this.showService.getSeasons(this.videoId).subscribe({
            next: value => {
              this.seasons = value;
            },
            error: err => {
              console.log(err);
            }
          });
        }
      },
      error: err => {
        console.log(err);
      }
    });
  }

  getStream(event:MatSelectChange){
    // this should use some rework here
    if(this.contentDetails.videoType === 'TV-SHOW') {
      this.showService.getStreamingLinkTvShow(this.videoId, event.value, '', '').subscribe({
        next: (result) => {
          this.videoSource = result;
        },
        error: (error) => {
          console.log(error);
        }
      });
    } else if (this.contentDetails.videoType === 'MOVIE') {
      this.movieService.getStreamingLinkMovie(this.videoId, event.value).subscribe({
        next: (result: string) => {
          this.videoSource = result;
        },
        error: (error) => {
         console.log(error)
        }
      });
    } else {
      alert('Error occurred');
    }
  }

  rateContent(rate: number){
    this.ratingService.rateContent(this.videoId, rate).subscribe({
      next: (value) => {
        console.log(value);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  subscribe(name: string, type: string) {
    console.log(name, type);
    this.subService.subscribe(type, name).subscribe({
      next: value => {
        console.log(value);
      },
      error: err => {
        console.log(err);
      }
    });
  }

  selectEpisode(event: MatSelectChange){
    this.selectedEpisode = this.episodesOfSeason.find(x => x.episodeNumber == event.value);
    console.log(this.selectedEpisode);
  }

  selectSeason(event: MatSelectChange){
    this.showService.getSeasonEpisodes(this.videoId, event.value).subscribe({
      next: (result) => {
        this.episodesOfSeason = result;
        // Maybe remove selected episode?
      },
      error: (error) => {
        console.log(error);
      }
    });

  }

  edit() {

  }

  delete() {

  }

  download() {
    // ovde bi trebalo da se javi da je korisnik preuzeo
    // radi update-a feed-a
    if (this.videoSource != '') window.open(this.videoSource);
  }
}
