import { NgModule } from '@angular/core';
import {BrowserModule, provideClientHydration, withNoHttpTransferCache} from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {MaterialModule} from "./material/material.module";
import {AuthModule} from "./auth/auth.module";
import {VideosModule} from "./videos/videos.module";
import { HttpClientModule, HTTP_INTERCEPTORS } from "@angular/common/http";
import {SubscriptionModule} from "./subscription/subscription.module";
import { ManageModule } from './videos/manage/manage.module';
import {CustomInterceptor} from "./auth/interceptor/custom.interceptor";

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
    SubscriptionModule,
    ManageModule,
  ],
  providers: [
    provideAnimationsAsync(),
    provideClientHydration(withNoHttpTransferCache()),
    { provide: HTTP_INTERCEPTORS, useClass: CustomInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
