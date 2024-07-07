import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from "./auth/login/login.component";
import { RegisterComponent } from "./auth/register/register.component";
import {HomeComponent} from "./videos/home/home.component";
import {VideoDetailsComponent} from "./videos/video-details/video-details.component";
import { CreateShowComponent } from './videos/create-show/create-show.component';
import {SubscriptionComponent} from "./subscription/subscription/subscription.component";

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: "register", component: RegisterComponent },
  { path: "login", component: LoginComponent },
  { path: "video/:videoType/:videoId", component: VideoDetailsComponent },
  { path: "createShow", component: CreateShowComponent},
  { path: "subscriptions", component: SubscriptionComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
