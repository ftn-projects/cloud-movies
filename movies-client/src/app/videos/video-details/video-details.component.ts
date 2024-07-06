import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {VideoService} from "../video.service";
import {MatSelectChange} from "@angular/material/select";

@Component({
  selector: 'app-video-details',
  templateUrl: './video-details.component.html',
  styleUrl: './video-details.component.css'
})
export class VideoDetailsComponent implements OnInit {
  videoId: string = '';
  videoType: string = '';
  videoSource: string = '';

  constructor(private route: ActivatedRoute,
              private videoService: VideoService) {
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.videoId = params.get('videoId') || '';
      this.videoType = params.get('videoType') || '';
    });
    // fetch the meta data, get id-s for video in different resolutions
  }

  getStream(event:MatSelectChange){
    this.videoService.getStreamingLink(this.videoId, this.videoType, event.value).subscribe({
      next: (result) => {
        this.videoSource = result;
        console.log(result);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }
}
