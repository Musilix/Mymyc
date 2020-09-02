import { TestBed } from '@angular/core/testing';

import { ShareLoadingService } from './share-loading.service';

describe('ShareLoadingService', () => {
  let service: ShareLoadingService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ShareLoadingService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
