import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-upload-video',
  templateUrl: './upload-video.component.html',
  styleUrl: './upload-video.component.css'
})
export class UploadVideoComponent {
  @Input('videoId') videoId?: string;
  @Input('season') season?: number;
  @Input('episode') episode?: number;
  @Input('uploadButton') uploadButton: boolean = true; 
  
  protected file?: File;

  onFileSelected(event: any): void {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      this.file = selectedFile;
    }
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const dropArea = event.currentTarget as HTMLElement;
    dropArea.style.backgroundColor = '#f1f1f1';
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const dropArea = event.currentTarget as HTMLElement;
    dropArea.style.backgroundColor = '#222831';
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const dropArea = event.currentTarget as HTMLElement;
    dropArea.style.backgroundColor = '#222831';

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.file = files[0];
    }
  }

  upload(): void {
    // Implement the file save logic here
    console.log('File saved:', this.file);
  }
}
