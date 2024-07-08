import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  constructor(private snackbar: MatSnackBar) {
  }

  displaySnack(text: string, action: string = 'OK') {
    console.log(text)
    this.snackbar.open(text, action, { duration: 0 });
  }
}
