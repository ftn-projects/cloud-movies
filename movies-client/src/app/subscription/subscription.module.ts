import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SubscriptionComponent } from './subscription/subscription.component';
import {MaterialModule} from "../material/material.module";



@NgModule({
  declarations: [
    SubscriptionComponent
  ],
  imports: [
    CommonModule,
    MaterialModule
  ]
})
export class SubscriptionModule { }
