import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {LoginComponent} from "./login/login.component";
import {RegisterComponent} from "./register/register.component";
import {MaterialModule} from "../material/material.module";
import { ReactiveFormsModule } from "@angular/forms";
import { NavbarComponent } from './navbar/navbar.component';
import {RouterLink} from "@angular/router";
import { NavbarAdminComponent } from './navbar-admin/navbar-admin.component';
import { NavbarUserComponent } from './navbar-user/navbar-user.component';


@NgModule({
  declarations: [
    LoginComponent,
    RegisterComponent,
    NavbarComponent,
    NavbarAdminComponent,
    NavbarUserComponent,
  ],
  imports: [
    CommonModule,
    MaterialModule,
    ReactiveFormsModule,
    RouterLink
  ],
  exports: [
    LoginComponent,
    RegisterComponent,
    NavbarComponent
  ]
})
export class AuthModule { }
