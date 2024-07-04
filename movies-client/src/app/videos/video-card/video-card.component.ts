import {Component, Input, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {Content} from "../models/content";

@Component({
  selector: 'app-video-card',
  templateUrl: './video-card.component.html',
  styleUrl: './video-card.component.css'
})
export class VideoCardComponent implements OnInit{

  @Input()
  videoId: string = ''

  @Input()
  content: Content ={
    title: '',
    videoId: '',
    videoType: '',
    actors: '',
    directors: '',
    releaseDate: '',
    description: '',
    duration: '',
    genres: '',
  }
  constructor(private router: Router) {
  }

  onCardClick(){
    this.router.navigate(['/video', this.content?.videoType, this.content?.videoId]);
  }

  getYear(): number {
    const date = new Date(this.content.releaseDate);
    return date.getFullYear();
  }
  ngOnInit(): void {

  }
}
