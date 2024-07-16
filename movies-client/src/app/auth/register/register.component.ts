import { Component } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {AuthenticationService} from "../authentication.service";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {

  registrationForm: FormGroup = new FormGroup({
    username: new FormControl('',[Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required]),
    firstName: new FormControl('', [Validators.required]),
    lastName: new FormControl('', [Validators.required]),
    birthdate: new FormControl('', [Validators.required]),
  });

  constructor(private authService: AuthenticationService) {
  }

  register(){
    this.authService.register(
      this.registrationForm.controls['username'].value,
      this.registrationForm.controls['email'].value,
      this.registrationForm.controls['password'].value,
      this.registrationForm.controls['birthdate'].value,
      this.registrationForm.controls['firstName'].value,
      this.registrationForm.controls['lastName'].value
    )
  }
}
