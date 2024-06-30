import {AfterViewInit, Component, OnInit} from '@angular/core';
import {AuthenticationService} from "../authentication.service";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent implements OnInit{
  userRole: string = '';

  constructor(private authService: AuthenticationService) {
  }

  logout() {
    this.authService.logout();
  }

  ngOnInit(): void {
    this.authService.userRoleState.subscribe((role) => {
        this.userRole = role;
      }
    );
    this.authService.getUserRole();
  }
}
