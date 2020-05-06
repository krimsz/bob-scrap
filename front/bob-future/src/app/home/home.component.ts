import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {PostService} from '../service/post.service';
import {Subject} from 'rxjs';
import {debounceTime, distinctUntilChanged} from 'rxjs/operators';
import {Router} from '@angular/router';
import {StateService} from '../service/state.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  posts = [];
  searchUpdated = new Subject();

  constructor(private postService: PostService, private changeDetectorRef: ChangeDetectorRef,
              private router: Router, private stateService: StateService) {
    this.searchUpdated.pipe(
      debounceTime(1000),
      distinctUntilChanged()
    ).subscribe( (searchTerm: string) => {
      this.postService.getPostsByQuery(searchTerm).subscribe( r => {
        this.posts = r['hits']['hits'].map(r => r["_source"]);
        this.stateService.setCurrentPostList(this.posts);
      });
      this.changeDetectorRef.detectChanges();
    });
  }

  ngOnInit() {
    this.posts = this.stateService.getCurrentPostList();
  }

  filterDocuments($event: any) {
    this.searchUpdated.next($event.target.value);
  }

  goToPost(id: any) {
    this.router.navigate(['/post/' + id]);
  }
}
