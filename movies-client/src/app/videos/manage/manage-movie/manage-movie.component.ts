import { Component, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-manage-movie',
  templateUrl: './manage-movie.component.html',
  styleUrl: './manage-movie.component.css'
})
export class ManageMovieComponent {
  protected movieId?: string;

  constructor(private activatedroute: ActivatedRoute) {
  }

  ngOnInit() {
    this.activatedroute.params.subscribe(params => this.movieId = params['movieId'])
  }
}
