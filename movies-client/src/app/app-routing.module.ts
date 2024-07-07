import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import {HomeComponent} from './videos/home/home.component';
import {VideoDetailsComponent} from './videos/video-details/video-details.component';
import { ManageMovieComponent } from './videos/manage/manage-movie/manage-movie.component';
import { ManageShowComponent } from './videos/manage/manage-show/manage-show.component';
import { ManageEpisodeComponent } from './videos/manage/manage-episode/manage-episode.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'video/:videoType/:videoId', component: VideoDetailsComponent },

  /* Videos management */
  { path: 'create/movie', component: ManageMovieComponent },
  { path: 'edit/movie/:movieId', component: ManageMovieComponent },
  { path: 'create/show', component: ManageShowComponent },
  { path: 'edit/show/:showId', component: ManageShowComponent },
  { path: 'create/episode/:showId/:season', component: ManageEpisodeComponent },
  { path: 'edit/episode/:showId/:season/:episode', component: ManageEpisodeComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
