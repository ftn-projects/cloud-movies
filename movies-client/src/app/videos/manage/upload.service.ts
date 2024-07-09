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
    return this.http.get<any>(environments.api + '/upload');
  }

  uploadFile(upload: any, file: Blob): Observable<void> {
    console.log(upload.uploadUrl)

    let formData = new FormData();
    for (const key in upload.uploadUrl.fields) {
      formData.append(key, upload.uploadUrl.fields[key]);
    }
    formData.append('file', file);
    formData.set('Content-Type', 'application/zip');

    return this.http.post<void>(upload.uploadUrl.url, formData);
  }
}
