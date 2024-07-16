import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import { VideoDetailsComponent } from './video-details/video-details.component';
import { MaterialModule } from "../material/material.module";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { VideoCardComponent } from './video-card/video-card.component';
import { RouterLink } from "@angular/router";


@NgModule({
  declarations: [
    HomeComponent,
    VideoDetailsComponent,
    VideoCardComponent
  ],
  imports: [
    CommonModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    RouterLink
  ]
})
export class VideosModule { }
