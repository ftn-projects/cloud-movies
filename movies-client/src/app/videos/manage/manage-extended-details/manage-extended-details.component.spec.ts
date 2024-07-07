import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageExtendedDetailsComponent } from './manage-extended-details.component';

describe('ManageExtendedDetailsComponent', () => {
  let component: ManageExtendedDetailsComponent;
  let fixture: ComponentFixture<ManageExtendedDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageExtendedDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ManageExtendedDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
