import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environments } from '../../../environments/evnironment';

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  constructor(private http: HttpClient) { }

  getUploadUrl(): Observable<any> {
    return this.http.get<any>(environments.api + '/uploadurl');
  }

  uploadFile(upload: any, file: Blob): Observable<void> {
    const formData = new FormData();
    Object.keys(upload.params).forEach(key => {
      formData.append(key, upload.params[key]);
    });
    formData.append('file', file);
    return this.http.post<void>(upload.url, formData);
  }
}
