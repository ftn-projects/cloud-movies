import { Component, Input, ViewChild } from '@angular/core';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';
import { provideNativeDateAdapter } from '@angular/material/core';
import { ActivatedRoute } from '@angular/router';
import { ContentService } from '../../content.service';
import { ManageBasicDetailsComponent } from '../manage-basic-details/manage-basic-details.component';
import { ManageExtendedDetailsComponent } from '../manage-extended-details/manage-extended-details.component';

@Component({
  selector: 'app-manage-show',
  templateUrl: './manage-show.component.html',
  styleUrl: './manage-show.component.css',
  providers: [provideNativeDateAdapter()]
})
export class ManageShowComponent {
  protected showId?: string;
  protected seasonsGroup: FormGroup;

  @ViewChild(ManageBasicDetailsComponent) basicDetailsComponent!: ManageBasicDetailsComponent;
  @ViewChild(ManageExtendedDetailsComponent) extendedDetailsComponent!: ManageExtendedDetailsComponent;

  constructor(
    private activatedroute: ActivatedRoute, 
    private formBuilder: FormBuilder,
    private contentService: ContentService
  ) {
    this.seasonsGroup = this.formBuilder.group({
      seasons: this.formBuilder.array([])
    });
  }

  ngOnInit() {
    this.activatedroute.params.subscribe(params => {
      this.showId = params['showId'];
      this.loadData();
    });
  }

  get seasons(): FormArray {
    return this.seasonsGroup.get('seasons') as FormArray;
  }

  getSeasonFormGroup(index: number): FormGroup {
    return this.seasons.at(index) as FormGroup;
  }

  addSeason(seasonName: string = '', releaseDate: string = '') {
    const seasonForm = this.formBuilder.group({
      seasonName: seasonName,
      releaseDate: releaseDate,
    });
    this.seasons.push(seasonForm);
  }

  removeSeason(index: number) {
    this.seasons.removeAt(index);
  }

  cancel() {
    this.loadData();
  }

  save() {
    const basicDetails = this.basicDetailsComponent.detailsGroup.value;
    const extendedDetails = this.extendedDetailsComponent.detailsGroup.value;
    const seasons = this.seasonsGroup.value;

    const show = {
      ...basicDetails,
      ...extendedDetails,
      seasons: seasons.seasons
    };

    // this.contentService.saveContentMetadata(show).subscribe(() => {
    //   console.log('Show saved');
    // });
  }

  loadData() {
    if (!this.showId) return;

    this.contentService.getContentMetadata(this.showId).subscribe(show => {
      this.basicDetailsComponent.loadData(show.title, show.description, show.releaseDate);
      this.extendedDetailsComponent.loadData(show.genres, show.actors, show.directors);
    });

    // this.contentService.getSeasons(this.showId).subscribe(seasons => {
    //   this.seasons.clear();
    //   seasons.forEach(season => {
    //     this.addSeason(season.seasonName, season.releaseDate);
    //   });
    // });
  }
}
