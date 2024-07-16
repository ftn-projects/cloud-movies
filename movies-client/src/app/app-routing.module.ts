import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from "./auth/login/login.component";
import { RegisterComponent } from "./auth/register/register.component";
import {HomeComponent} from "./videos/home/home.component";
import {VideoDetailsComponent} from "./videos/video-details/video-details.component";
import {SubscriptionComponent} from "./subscription/subscription/subscription.component";
import { ManageMovieComponent } from './videos/manage/manage-movie/manage-movie.component';
import { ManageEpisodeComponent } from './videos/manage/manage-episode/manage-episode.component';
import { ManageShowComponent } from './videos/manage/manage-show/manage-show.component';
import {authGuard} from "./auth/guard/auth.guard";

const routes: Routes = [
  { path: '', component: HomeComponent, canActivate: [authGuard] },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'video/:videoId', component: VideoDetailsComponent, canActivate: [authGuard] },
  { path: "subscriptions", component: SubscriptionComponent, canActivate: [authGuard] },
  /* Videos management */
  { path: 'create/movie', component: ManageMovieComponent, canActivate: [authGuard] },
  { path: 'edit/movie/:movieId', component: ManageMovieComponent, canActivate: [authGuard] },
  { path: 'create/show', component: ManageShowComponent, canActivate: [authGuard] },
  { path: 'edit/show/:showId', component: ManageShowComponent, canActivate: [authGuard] },
  { path: 'create/episode/:showId/:season', component: ManageEpisodeComponent, canActivate: [authGuard] },
  { path: 'edit/episode/:showId/:season/:episode', component: ManageEpisodeComponent, canActivate: [authGuard] }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
