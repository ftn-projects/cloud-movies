import { Component, ViewChild } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { provideNativeDateAdapter } from '@angular/material/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ContentService } from '../../content.service';
import { ManageBasicDetailsComponent } from '../manage-basic-details/manage-basic-details.component';
import { ManageExtendedDetailsComponent } from '../manage-extended-details/manage-extended-details.component';
import { ShowService } from '../../show.service';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';
import { SharedService } from '../../../shared/shared.service';

@Component({
  selector: 'app-manage-show',
  templateUrl: './manage-show.component.html',
  styleUrls: ['./manage-show.component.css'],
  providers: [provideNativeDateAdapter()]
})
export class ManageShowComponent {
  protected showId?: string;
  protected createSeason: FormGroup = new FormGroup({
    seasonTitle: new FormControl('', [Validators.required]),
    releaseDate: new FormControl('', [Validators.required])
  });
  get titleInput() { return this.createSeason.get('seasonTitle')?.value; }
  get releaseDateInput() { return this.createSeason.get('releaseDate')?.value; }

  protected seasons: any[] = [];

  @ViewChild(ManageBasicDetailsComponent) basicDetailsComponent!: ManageBasicDetailsComponent;
  @ViewChild(ManageExtendedDetailsComponent) extendedDetailsComponent!: ManageExtendedDetailsComponent;

  constructor(
    private activatedroute: ActivatedRoute,
    private contentService: ContentService,
    private showService: ShowService,
    private sharedService: SharedService,
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

  collectDetails(): any {
    const basicDetails = this.basicDetailsComponent.detailsGroup.value;
    const extendedDetails = this.extendedDetailsComponent.detailsGroup.value;

    return {
      ...basicDetails,
      'genres': extendedDetails.genres.split(',').map((genre: string) => genre.trim()),
      'actors': extendedDetails.actors.split(',').map((actor: string) => actor.trim()),
      'directors': extendedDetails.directors.split(',').map((director: string) => director.trim())
    };
  }

  createShow() {
    this.showService.createShow(this.collectDetails()).subscribe(showId => {
      this.sharedService.displaySnack('Show created');
      this.router.navigate([`/edit/show/${showId}`]);
    });
  }

  cancelDetails() {
    this.loadDetails();
  }

  updateDetails() {
    this.contentService.saveDetails(this.showId!, this.collectDetails()).subscribe((updated) => {
      this.sharedService.displaySnack('Show details updated');
      this.basicDetailsComponent.loadData(updated.title, updated.description, updated.releaseDate);
      this.extendedDetailsComponent.loadData(updated.genres, updated.actors, updated.directors);
    });
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

    this.showService.getSeasonsWithEpisodes(this.showId).subscribe(seasons => this.seasons = seasons);
  }

  addSeason() {
    if (this.createSeason.invalid) return;
    
    const title = this.titleInput;
    const releaseDate = this.releaseDateInput;

    this.showService.addSeason(this.showId!, title, releaseDate).subscribe(() => {
      this.sharedService.displaySnack('Season created');
      this.seasons.push({ title, releaseDate, episodes: [] });
      this.createSeason.reset();
    });
  }

  deleteSeason(season: number) {
    this.showService.deleteSeason(this.showId!, season).subscribe(() => {
      this.sharedService.displaySnack('Season deleted');
      this.seasons.splice(season, 1);
    });
  }

  getEpisodesForSeason(index: number) {
    return this.seasons[index].episodes;
  }

  addEpisode(season: number) {
    this.router.navigate([`/create/episode/${this.showId}/${season}`]);
  }

  editEpisode(episode: number, season: number) {
    this.router.navigate([`/edit/episode/${this.showId}/${season}/${episode}`]);
  }

  deleteEpisode(episode: number, season: number) {
    this.showService.deleteEpisode(this.showId!, season, episode).subscribe(() => {
      this.sharedService.displaySnack('Episode deleted');
      this.seasons[season].episodes.splice(episode, 1);
    });
  }

  deleteShow() {
    this.showService.deleteShow(this.showId!).subscribe(() => {
      this.sharedService.displaySnack('Show deleted');
      this.router.navigate(['/']);
    });
  }

  dropSeason(event: CdkDragDrop<string[]>) {
    const [first, second] = [event.previousIndex, event.currentIndex];

    this.showService.swapSeasons(this.showId!, first, second).subscribe(() => {
      console.log('Season order updated');
      moveItemInArray(this.seasons, first, second);
    });
  }

  dropEpisode(event: CdkDragDrop<string[]>, season: number) {
    const [first, second] = [event.previousIndex, event.currentIndex];

    this.showService.swapEpisodes(this.showId!, season, first, second).subscribe(() => {
      console.log('Episode order updated');
      moveItemInArray(this.seasons[season].episodes, event.previousIndex, event.currentIndex);
    });
  }
}
