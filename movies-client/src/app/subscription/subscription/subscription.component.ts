import {Component, OnInit} from '@angular/core';
import {UserSubs} from "../model/user-subs";
import {SubscriptionService} from "../subscription.service";

@Component({
  selector: 'app-subscription',
  templateUrl: './subscription.component.html',
  styleUrl: './subscription.component.css'
})
export class SubscriptionComponent implements OnInit{

  userSubscriptions: UserSubs = {
    actors: ['Some actor',],
    directors: ['Some director'],
    shows: ['Some show'],
    genres: ['Some genre'],
  }

  constructor(private subscriptionService: SubscriptionService) {
  }

  ngOnInit(): void {
    this.subscriptionService.getSubscriptions().subscribe({
      next: (data: UserSubs) => {
        this.userSubscriptions = data;
      },
      error: error => {
        console.log(error);
      }
    });
  }

  unsubscribe(name: string, type: string) {
    this.subscriptionService.unsubscribe(type, name).subscribe({
      next: (info: string) => {
        alert(info);
      },
      error: (err) => {
        console.log(err);
      }
    });
  }
}
