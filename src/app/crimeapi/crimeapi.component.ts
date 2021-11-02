import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { analyzeAndValidateNgModules } from '@angular/compiler';

@Component({
  selector: 'app-crimeapi',
  templateUrl: './crimeapi.component.html',
  styleUrls: ['./crimeapi.component.css']
})
export class CrimeapiComponent implements OnInit {

  url = 'https://api.usa.gov/crime/fbi/sapi//api/summarized/agencies/FL0500500/offenses/2019/2020?api_key=nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315';
  items = [];
  keynames = [];
  ori: string;
  fromstr: string;
  tostr: string;
  from: number;
  to: number;
  returnedstuff;
  specificcrimedata: object;


  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) {
    this.returnedstuff = new Object;
    this.specificcrimedata = new Object;
    this.ori = '';
    this.from = 0;
    this.to = 0;
    this.fromstr = '';
    this.tostr = '';


    this.route.queryParams
    .subscribe(params => {
      this.ori = params['ori'];
      this.fromstr = params['from'];
      this.from = this.fromstr ? (parseInt(params['from']) ? parseInt(params['from']) : new Date().getFullYear() - 5) : new Date().getFullYear() - 5;
      this.tostr = params['to'];
      this.to = this.tostr ? (parseInt(params['to']) ? parseInt(params['to']) : new Date().getFullYear()) : new Date().getFullYear();
      if(params['from'] != parseInt(params['from']) || params['to'] != parseInt(params['to']))
      {
        this.router.navigate(['crimeapi'], {queryParams: {ori: this.ori, from: this.from, to: this.to}}).then(()=>{window.location.reload()});
      }
      if(this.from > this.to)
      {
        var temp = this.to;
        this.to = this.from;
        this.from = temp;
        this.router.navigate(['crimeapi'], {queryParams: {ori: this.ori, from: this.from, to: this.to}}).then(()=>{window.location.reload()});
      }
    });

    this.url = 'https://api.usa.gov/crime/fbi/sapi//api/summarized/agencies/'
    this.url += this.ori
    this.url += '/offenses/'
    this.url += this.fromstr
    this.url += '/'
    this.url += this.tostr
    this.url+= '?api_key=nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315';

    this.http.get(this.url).toPromise().then(data =>{
      console.log(data);
      for (let key in data){
        if(data.hasOwnProperty(key)){
          var str : string;
          str = '';
          var str2 : string;
          str2 = JSON.stringify(key);
          str += str2;
          str += ": ";
          str += JSON.stringify(data[key as never]);
          this.items.push(str as never);
        }
      }
    });
   }

  ngOnInit(): void {
    
  }

}