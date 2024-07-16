import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { provideNativeDateAdapter } from '@angular/material/core';

@Component({
  selector: 'app-manage-basic-details',
  templateUrl: './manage-basic-details.component.html',
  styleUrl: './manage-basic-details.component.css',
  providers: [provideNativeDateAdapter()],
})
export class ManageBasicDetailsComponent {
  	detailsGroup: FormGroup = new FormGroup({
		title: new FormControl('',[Validators.required]),
		description: new FormControl('',[Validators.required]),
		releaseDate: new FormControl('',[Validators.required])
	});

	get titleInput() { return this.detailsGroup.get('title')?.value; }
	get descriptionInput() { return this.detailsGroup.get('description')?.value; }
	get releaseDateInput() { return this.detailsGroup.get('releaseDate')?.value; }

	loadData(title: string, description: string, releaseDate: string) {
		this.detailsGroup.setValue({
			title: title,
			description: description,
			releaseDate: releaseDate
		});
	}
}
