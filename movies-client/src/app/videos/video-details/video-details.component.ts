import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-video-details',
  templateUrl: './video-details.component.html',
  styleUrl: './video-details.component.css'
})
export class VideoDetailsComponent implements OnInit {
  videoId: string | null = '';
  videoType: string | null = '';

  constructor(private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.videoId = params.get('videoId');
      this.videoType = params.get('videoType');
    });
    // fetch the meta data, get id-s for video in different resolutions
  }

}
