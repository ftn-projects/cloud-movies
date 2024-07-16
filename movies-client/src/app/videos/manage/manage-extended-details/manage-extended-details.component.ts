import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-manage-extended-details',
  templateUrl: './manage-extended-details.component.html',
  styleUrl: './manage-extended-details.component.css'
})
export class ManageExtendedDetailsComponent {
    detailsGroup: FormGroup = new FormGroup({
		genres: new FormControl('',[Validators.required]),
		actors: new FormControl('',[Validators.required]),
		directors: new FormControl('',[Validators.required]),
	});

	get genresInput() { return this.detailsGroup.get('genres')?.value; }
	get actorsInput() { return this.detailsGroup.get('actors')?.value; }
	get directorsInput() { return this.detailsGroup.get('directors')?.value; }

	loadData(genres: string[], actors: string[], directors: string[]) {
		this.detailsGroup.setValue({
			genres: genres.join(', '),
			actors: actors.join(', '),
			directors: directors.join(', ')
		});
	}
}
