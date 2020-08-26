import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ScenarioTableComponent } from './scenario-table.component';

describe('ScenarioTableComponent', () => {
  let component: ScenarioTableComponent;
  let fixture: ComponentFixture<ScenarioTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ScenarioTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ScenarioTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
