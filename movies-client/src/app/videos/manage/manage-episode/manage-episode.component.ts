import { Component, Input, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ManageBasicDetailsComponent } from '../manage-basic-details/manage-basic-details.component';
import { ContentService } from '../../content.service';
import { UploadVideoComponent } from '../upload-video/upload-video.component';
import { UploadService } from '../upload.service';
import { ShowService } from '../../show.service';
import JSZip from 'jszip';
import { SharedService } from '../../../shared/shared.service';

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
    private showService: ShowService,
    private uploadService: UploadService,
    private sharedService: SharedService,
    private router: Router
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
  @ViewChild(UploadVideoComponent) uploadVideoComponent!: UploadVideoComponent;

  collectDetails(): any {
    return this.basicDetailsComponent.detailsGroup.value;
  }

  cancelDetails() {
    this.loadData();
  }

  updateDetails() {
    this.showService.saveEpisodeDetails(this.showId!, this.season!, this.episode!, this.collectDetails()).subscribe((updated) => {
      this.sharedService.displaySnack('Episode details updated');
      this.basicDetailsComponent.loadData(updated.title, updated.description, updated.releaseDate);
    });
  }

  createEpisode() {
    if (this.basicDetailsComponent.detailsGroup.invalid) {
      this.sharedService.displaySnack('Invalid form data');
      return;
    }

    if (!this.getFile()) {
      this.sharedService.displaySnack('No file selected');
      return;
    }

    this.uploadService.getUploadUrl().subscribe(upload => {
      const detailsJson = new Blob([JSON.stringify(this.collectDetails())], { type: 'application/json' });
      const details = new File([detailsJson], 'details.json');
      const video = this.getFile()!;

      const zip = new JSZip();
      zip.file('details.json', details);
      zip.file(video.name, video);

      zip.generateAsync({ type: 'blob' }).then((zip) => {
        this.uploadEpisode(upload, zip);
      });
    });
  }

  updateVideo() {
    if (!this.getFile()) {
      this.sharedService.displaySnack('No file selected');
      return;
    }

    this.uploadService.getUploadUrl().subscribe(upload => this.uploadEpisode(upload, this.getFile()!));
  }

  uploadEpisode(upload: any, file: Blob) {
    this.uploadService.uploadFile(upload, file).subscribe(() => {
      this.sharedService.displaySnack('Episode uploaded and is being processed');
      this.router.navigate(['/']);
    });
  }

  loadData() {
    if (!this.showId || !this.season || !this.episode) return;

    this.showService.getEpisodeDetails(this.showId!, this.season!, this.episode!).subscribe(episode => {
      this.basicDetailsComponent.loadData(episode.title, episode.description, episode.releaseDate);
    });
  }

  deleteEpisode() {
    this.showService.deleteEpisode(this.showId!, this.season!, this.episode!).subscribe(() => {
      this.sharedService.displaySnack('Episode deleted');
      this.router.navigate(['/edit/show/' + this.showId + '/' + this.season]);
    });
  }

  getFile() {
    return this.uploadVideoComponent?.file;
  }
}
