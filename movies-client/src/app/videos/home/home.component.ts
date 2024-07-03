import { Component } from '@angular/core';
import {FormControl} from "@angular/forms";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

  searchText: string = '';
  constructor() {
  }
  onSubmit() {
    alert('beep boop');
  }
}
