import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageShowComponent } from './manage-show.component';

describe('ManageShowComponent', () => {
  let component: ManageShowComponent;
  let fixture: ComponentFixture<ManageShowComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageShowComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ManageShowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
