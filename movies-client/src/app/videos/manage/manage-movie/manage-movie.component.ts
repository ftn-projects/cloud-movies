import { Component, Input, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ContentService } from '../../content.service';
import { ManageBasicDetailsComponent } from '../manage-basic-details/manage-basic-details.component';
import { ManageExtendedDetailsComponent } from '../manage-extended-details/manage-extended-details.component';

@Component({
  selector: 'app-manage-movie',
  templateUrl: './manage-movie.component.html',
  styleUrl: './manage-movie.component.css'
})
export class ManageMovieComponent {
  protected movieId?: string;

  constructor(
    private activatedroute: ActivatedRoute,
    private contentService: ContentService
  ) {
  }

  ngOnInit() {
    this.activatedroute.params.subscribe(params => this.movieId = params['movieId'])
  }

  @ViewChild(ManageBasicDetailsComponent) basicDetailsComponent!: ManageBasicDetailsComponent;
  @ViewChild(ManageExtendedDetailsComponent) extendedDetailsComponent!: ManageExtendedDetailsComponent;

  cancelDetails() {
    this.loadData();
  }

  updateDetails() {
    const basicDetails = this.basicDetailsComponent.detailsGroup.value;
    const extendedDetails = this.extendedDetailsComponent.detailsGroup.value;

    const movie = {
      ...basicDetails,
      ...extendedDetails,
    };

    // this.contentService.saveContentMetadata(movie).subscribe(() => {
    //   console.log('Movie saved');
    // });
  }

  createMovie() {
  }

  loadData() {
    if (!this.movieId) return;

    this.contentService.getContentMetadata(this.movieId).subscribe(movie => {
      this.basicDetailsComponent.loadData(movie.title, movie.description, movie.releaseDate);
      this.extendedDetailsComponent.loadData(movie.genres, movie.actors, movie.directors);
    });
  }

  deleteMovie() {
    
  }
}
