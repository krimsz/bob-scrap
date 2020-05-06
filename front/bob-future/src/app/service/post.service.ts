import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PostService {

  constructor(private httpClient: HttpClient) { }

  private generateQuery(query: string) {
    return  {
      from: 0,
      size: 1000,
      query:
        {
          multi_match:
            {
              operator: 'or',
              query,
              fuzziness: 'AUTO',
              fields: ['title', 'sanitized_content', 'comments.sanitized_content']
            }
        }
    };
  }

  getPostsByQuery(query: string) {
    return this.httpClient.post(environment.esURL + '/_search', this.generateQuery(query));
  }
}
