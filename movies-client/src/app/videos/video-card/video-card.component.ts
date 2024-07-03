import {Component, Input} from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-video-card',
  templateUrl: './video-card.component.html',
  styleUrl: './video-card.component.css'
})
export class VideoCardComponent {

  @Input()
  videoId: string = ''

  constructor(private router: Router) {
  }

  onCardClick(){
    this.router.navigate(['/video', this.videoId]);
  }
}
