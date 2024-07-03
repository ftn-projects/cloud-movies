import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-create-show',
  templateUrl: './create-show.component.html',
  styleUrl: './create-show.component.css'
})

export class CreateShowComponent {
	showGroup : FormGroup = new FormGroup({
		title: new FormControl('',[Validators.required]),
		description: new FormControl('',[Validators.required]),
		genres: new FormControl('',[Validators.required]),
		actors: new FormControl('',[Validators.required]),
		directors: new FormControl('',[Validators.required]),
		year: new FormControl('',[Validators.required])
	});

	get titleInput() { return this.showGroup.get('title')?.value; }
	get descriptionInput() { return this.showGroup.get('description')?.value; }
	get genresInput() { return this.showGroup.get('genres')?.value; }
	get actorsInput() { return this.showGroup.get('actors')?.value; }
	get directorsInput() { return this.showGroup.get('directors')?.value; }
	get yearInput() { return this.showGroup.get('year')?.value; }
}
