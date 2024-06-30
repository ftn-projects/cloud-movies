import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from "@angular/forms";
import {AuthenticationService} from "../authentication.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  credentialsForm : FormGroup = new FormGroup({
    email: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required])
  });

  constructor(private authService: AuthenticationService) {
  }

  login(){
    if (this.credentialsForm.valid){
      this.authService.login(this.credentialsForm.controls['email'].value, this.credentialsForm.controls['password'].value);
    }
  }
}
