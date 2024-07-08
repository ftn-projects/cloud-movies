import { Component, ViewChild } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { provideNativeDateAdapter } from '@angular/material/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ContentService } from '../../content.service';
import { ManageBasicDetailsComponent } from '../manage-basic-details/manage-basic-details.component';
import { ManageExtendedDetailsComponent } from '../manage-extended-details/manage-extended-details.component';
import { ShowService } from '../../show.service';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-manage-show',
  templateUrl: './manage-show.component.html',
  styleUrls: ['./manage-show.component.css'],
  providers: [provideNativeDateAdapter()]
})
export class ManageShowComponent {
  protected showId?: string;
  protected createSeason: FormGroup = new FormGroup({
    seasonName: new FormControl('', [Validators.required]),
    releaseDate: new FormControl('', [Validators.required])
  });
  get titleInput() { return this.createSeason.get('seasonName')?.value; }
  get releaseDateInput() { return this.createSeason.get('releaseDate')?.value; }

  protected seasonDetails: any[] = [];

  @ViewChild(ManageBasicDetailsComponent) basicDetailsComponent!: ManageBasicDetailsComponent;
  @ViewChild(ManageExtendedDetailsComponent) extendedDetailsComponent!: ManageExtendedDetailsComponent;

  constructor(
    private activatedroute: ActivatedRoute,
    private formBuilder: FormBuilder,
    private contentService: ContentService,
    private showService: ShowService,
    private router: Router
  ) {
  }

  ngOnInit() {
    this.activatedroute.params.subscribe(params => {
      this.showId = params['showId'];
      this.loadDetails();
      this.loadSeasons();
    });
  }

  createShow() {
    throw new Error('Method not implemented.');
  }

  cancelDetails() {
    this.loadDetails();
  }

  updateDetails() {
    const basicDetails = this.basicDetailsComponent.detailsGroup.value;
    const extendedDetails = this.extendedDetailsComponent.detailsGroup.value;

    const show = {
      ...basicDetails,
      ...extendedDetails,
    };

    // this.contentService.saveContentMetadata(show).subscribe(() => {
    //   console.log('Show saved');
    // });
  }

  loadDetails() {
    if (!this.showId) return;

    this.contentService.getContentMetadata(this.showId).subscribe(show => {
      this.basicDetailsComponent.loadData(show.title, show.description, show.releaseDate);
      this.extendedDetailsComponent.loadData(show.genres, show.actors, show.directors);
    });
  }

  loadSeasons() {
    if (!this.showId) return;

    this.showService.getSeasonsWithEpisodes(this.showId).subscribe((seasons: any[]) => {
      this.seasonDetails = seasons;
    });
  }

  addSeason() {
    const seasonName = this.titleInput;
    const releaseDate = this.releaseDateInput;
    if (seasonName && releaseDate) {
      this.seasonDetails.push({ seasonName, releaseDate, episodes: [] });
      this.createSeason.reset();
    }
  }

  deleteSeason(index: number) {
    this.seasonDetails.splice(index, 1);
  }

  getEpisodesForSeason(index: number) {
    return this.seasonDetails[index].episodes;
  }

  addEpisode(seasonIndex: number) {
    this.router.navigate([`/create/episode/${this.showId}/${seasonIndex}`]);
  }

  editEpisode(episodeIndex: number, seasonIndex: number) {
    this.router.navigate([`/edit/episode/${this.showId}/${seasonIndex}/${episodeIndex}`]);
  }

  deleteEpisode(episodeIndex: number, seasonIndex: number) {
    this.seasonDetails[seasonIndex].episodes.splice(episodeIndex, 1);
  }

  deleteShow() {
    // call api to delete
  }

  dropSeason(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.seasonDetails, event.previousIndex, event.currentIndex);

    // Update the season numbers in the service
    // this.showService.swapSeason(this.showId!, this.originalSeasonOrder, this.seasonDetails).subscribe(() => {
    // });
  }
}
