import {Component, OnInit} from '@angular/core';
import {FormControl} from "@angular/forms";
import {VideoService} from "../video.service";
import {Content} from "../models/content";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {

  searchText: string = '';
  homepageContent: Content[] = []
  constructor(private videoService: VideoService) {}

  onSubmit() {
    alert('beep boop');
  }

  ngOnInit(): void {
    // should check for a role first
    this.videoService.getContentAdmin().subscribe({
      next: (result) => {
          this.homepageContent = result;
      },
      error: (error) => {
        console.log(error)
      }
    });
  }
}
