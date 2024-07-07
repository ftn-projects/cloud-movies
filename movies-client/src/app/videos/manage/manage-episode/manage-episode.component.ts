import { Component, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-manage-episode',
  templateUrl: './manage-episode.component.html',
  styleUrl: './manage-episode.component.css'
})
export class ManageEpisodeComponent {
  protected showId?: string;
  protected season?: string;
  protected episode?: string;

  constructor(private activatedroute: ActivatedRoute) {
  }

  ngOnInit() {
    this.activatedroute.params.subscribe(params => {
      this.showId = params['showId'];
      this.season = params['season'];
      this.episode = params['episode'];
    });
  }

  protected create = () => !this.showId || !this.season || !this.episode;
}
