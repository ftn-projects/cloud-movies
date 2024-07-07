import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageBasicDetailsComponent } from './manage-basic-details.component';

describe('ManageBasicDetailsComponent', () => {
  let component: ManageBasicDetailsComponent;
  let fixture: ComponentFixture<ManageBasicDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageBasicDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ManageBasicDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
