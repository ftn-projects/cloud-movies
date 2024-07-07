import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageEpisodeComponent } from './manage-episode.component';

describe('ManageEpisodeComponent', () => {
  let component: ManageEpisodeComponent;
  let fixture: ComponentFixture<ManageEpisodeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageEpisodeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ManageEpisodeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
