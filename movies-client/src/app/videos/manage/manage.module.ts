import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManageBasicDetailsComponent } from './manage-basic-details/manage-basic-details.component';
import { ManageExtendedDetailsComponent } from './manage-extended-details/manage-extended-details.component';
import { UploadVideoComponent } from './upload-video/upload-video.component';
import { ManageEpisodeComponent } from './manage-episode/manage-episode.component';
import { ManageMovieComponent } from './manage-movie/manage-movie.component';
import { ManageShowComponent } from './manage-show/manage-show.component';
import { ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../material/material.module';
import { RouterModule } from '@angular/router';
import { DragDropModule } from '@angular/cdk/drag-drop';



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
    CommonModule,
    MaterialModule,
    ReactiveFormsModule,
    RouterModule,
    DragDropModule
  ]
})
export class ManageModule { }
