import { Component, Input, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ManageBasicDetailsComponent } from '../manage-basic-details/manage-basic-details.component';
import { ContentService } from '../../content.service';

@Component({
  selector: 'app-manage-episode',
  templateUrl: './manage-episode.component.html',
  styleUrl: './manage-episode.component.css'
})
export class ManageEpisodeComponent {
  protected showId?: string;
  protected season?: number;
  protected episode?: number;

  constructor(
    private activatedroute: ActivatedRoute,
    private contentService: ContentService
  ) {
  }

  ngOnInit() {
    this.activatedroute.params.subscribe(params => {
      this.showId = params['showId'];
      this.season = params['season'];
      this.episode = params['episode'];
      this.loadData();
    });
  }

  @ViewChild(ManageBasicDetailsComponent) basicDetailsComponent!: ManageBasicDetailsComponent;

  cancel() {
    this.loadData();
  }

  save() {
    const basicDetails = this.basicDetailsComponent.detailsGroup.value;

    const movie = {
      ...basicDetails,
    };

    // this.contentService.saveContentMetadata(movie).subscribe(() => {
    //   console.log('Movie saved');
    // });
  }

  create() {
  }

  loadData() {
    if (!this.showId || !this.season || !this.episode) return;

    // this.contentService.getEpisode(this.showId, this.season, this.episode).subscribe(episode => {
    //   this.basicDetailsComponent.loadData(episode.title, episode.description, episode.releaseDate);
    // });
  }
}
