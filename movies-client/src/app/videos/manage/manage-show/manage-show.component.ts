import { Component, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-manage-show',
  templateUrl: './manage-show.component.html',
  styleUrl: './manage-show.component.css'
})
export class ManageShowComponent {
  protected showId?: string;

  constructor(private activatedroute: ActivatedRoute) {
  }

  ngOnInit() {
    this.activatedroute.params.subscribe(params => this.showId = params['showId'])
  }
}
