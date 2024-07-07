import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManageBasicDetailsComponent } from './manage-basic-details/manage-basic-details.component';
import { ManageExtendedDetailsComponent } from './manage-extended-details/manage-extended-details.component';
import { UploadVideoComponent } from './upload-video/upload-video.component';
import { ManageEpisodeComponent } from './manage-episode/manage-episode.component';
import { ManageMovieComponent } from './manage-movie/manage-movie.component';
import { ManageShowComponent } from './manage-show/manage-show.component';



@NgModule({
  declarations: [
    ManageBasicDetailsComponent,
    ManageExtendedDetailsComponent,
    UploadVideoComponent,
    ManageEpisodeComponent,
    ManageMovieComponent,
    ManageShowComponent
  ],
  imports: [
    CommonModule
  ]
})
export class ManageModule { }
