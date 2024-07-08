import { Component, Input, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ContentService } from '../../content.service';
import { ManageBasicDetailsComponent } from '../manage-basic-details/manage-basic-details.component';
import { ManageExtendedDetailsComponent } from '../manage-extended-details/manage-extended-details.component';
import { UploadVideoComponent } from '../upload-video/upload-video.component';
import { UploadService } from '../upload.service';
import JSZip from 'jszip';
import { MovieService } from '../../movie.service';
import { SharedService } from '../../../shared/shared.service';

@Component({
  selector: 'app-manage-movie',
  templateUrl: './manage-movie.component.html',
  styleUrl: './manage-movie.component.css'
})
export class ManageMovieComponent {
  protected movieId?: string;

  constructor(
    private activatedroute: ActivatedRoute,
    private uploadService: UploadService,
    private contentService: ContentService,
    private movieService: MovieService,
    private sharedService: SharedService,
    private router: Router
  ) {
  }

  ngOnInit() {
    this.activatedroute.params.subscribe(params => this.movieId = params['movieId'])
  }

  @ViewChild(ManageBasicDetailsComponent) basicDetailsComponent!: ManageBasicDetailsComponent;
  @ViewChild(ManageExtendedDetailsComponent) extendedDetailsComponent!: ManageExtendedDetailsComponent;
  @ViewChild(UploadVideoComponent) uploadVideoComponent!: UploadVideoComponent;

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

  cancelDetails() {
    this.loadData();
  }

  updateDetails() {
    this.contentService.saveDetails(this.movieId!, this.collectDetails()).subscribe((updated) => {
      this.sharedService.displaySnack('Movie details updated');
      this.basicDetailsComponent.loadData(updated.title, updated.description, updated.releaseDate);
      this.extendedDetailsComponent.loadData(updated.genres, updated.actors, updated.directors);
    });
  }

  createMovie() {
    if (this.basicDetailsComponent.detailsGroup.invalid || this.extendedDetailsComponent.detailsGroup.invalid) {
      this.sharedService.displaySnack('Invalid form data');
      return;
    }

    if (!this.uploadVideoComponent.file) {
      this.sharedService.displaySnack('No file selected');
      return;
    }

    this.uploadService.getUploadUrl().subscribe(upload => {
      const detailsJson = new Blob([JSON.stringify(this.collectDetails())], { type: 'application/json' });
      const details = new File([detailsJson], 'details.json');
      const video = this.uploadVideoComponent.file!;

      const zip = new JSZip();
      zip.file('details.json', details);
      zip.file(video.name, video);

      zip.generateAsync({ type: 'blob' }).then((zip) => {
        this.uploadMovie(upload, zip);
      });
    });
  }

  updateVideo() {
    if (!this.getFile()) {
      this.sharedService.displaySnack('No file selected');
      return;
    }

    this.uploadService.getUploadUrl().subscribe(upload => this.uploadMovie(upload, this.getFile()!));
  }

  uploadMovie(upload: any, video: Blob) {
    this.uploadService.uploadFile(upload, video).subscribe(() => {
      this.sharedService.displaySnack('Movie uploaded and is being processed');
      this.router.navigate(['/']);
    });
  }

  loadData() {
    if (!this.movieId) return;

    this.contentService.getContentMetadata(this.movieId).subscribe(movie => {
      this.basicDetailsComponent.loadData(movie.title, movie.description, movie.releaseDate);
      this.extendedDetailsComponent.loadData(movie.genres, movie.actors, movie.directors);
    });
  }

  deleteMovie() {
    this.movieService.deleteMovie(this.movieId!).subscribe(() => {
      this.sharedService.displaySnack('Movie deleted');
      this.router.navigate(['/']);
    });
  }

  getFile() {
    return this.uploadVideoComponent?.file;
  }
}
