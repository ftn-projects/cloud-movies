import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import { VideoDetailsComponent } from './video-details/video-details.component';
import {MaterialModule} from "../material/material.module";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { VideoCardComponent } from './video-card/video-card.component';
import {RouterLink} from "@angular/router";
import { CreateShowComponent } from './create-show/create-show.component';


@NgModule({
  declarations: [
    HomeComponent,
    VideoDetailsComponent,
    VideoCardComponent,
    CreateShowComponent
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
