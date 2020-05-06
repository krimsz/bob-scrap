import {Component, OnInit} from '@angular/core';
import {StateService} from '../service/state.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent implements OnInit {
  post: any;
  constructor(private stateService: StateService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    console.log(id);
    console.log(this.stateService.getCurrentPostList());
    this.post = this.stateService.getCurrentPostList().filter(p => p.id === id.toString())[0];
  }

}
