import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {MaterialModule} from "./material/material.module";
import {AuthModule} from "./auth/auth.module";
import {VideosModule} from "./videos/videos.module";
import { HttpClientModule, HTTP_INTERCEPTORS } from "@angular/common/http";
import { ManageModule } from './videos/manage/manage.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AuthModule,
    VideosModule,
    MaterialModule,
    HttpClientModule,
    ManageModule
  ],
  providers: [
    provideAnimationsAsync(),
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
