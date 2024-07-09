import {CanActivateFn, Router, UrlSegment} from '@angular/router';
import {AuthenticationService} from "../authentication.service";
import { inject } from "@angular/core"
import {UserPaths} from "./user.paths";
import {AdminPaths} from "./admin.paths";
export const authGuard: CanActivateFn = (route, state) => {
  const authService: AuthenticationService = inject(AuthenticationService);
  const router: Router = inject(Router);
  const path: string = getFullPath(route.url);
  const userRole: string = authService.userRole$.getValue();

  if (userRole === 'Admin' && checkForPaths(path, AdminPaths)) return true;
  else if (userRole === 'User' && checkForPaths(path, UserPaths)) return true;
  else {
    router.navigate(['/login']);
    return false;
  }

};

function getFullPath(urlSegments: UrlSegment[]): string {
  let path = '';
  for (const urlSegment of urlSegments) {
    path += urlSegment.path + '/';
  }
  return path;
}

function checkForPaths(accessedPath: string, paths: string[]): boolean {
  for (const path of paths) {
    if (accessedPath.includes(path)) return true;
  }
  return false;
}
