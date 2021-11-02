import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { PropertiesComponent } from "./properties/properties.component";
import { PropertyBrowserComponent } from "./properties/property-browser/property-browser.component";
import { PropertyViewerComponent } from "./properties/property-viewer/property-viewer.component";
import { HomeComponent } from './home/home.component';
import { MapComponent } from './map/map.component';
import { CrimeapiComponent } from './crimeapi/crimeapi.component';

const routes: Routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'home', component: HomeComponent },
    { path: 'map', component: MapComponent },
    { path: 'property', component: PropertiesComponent, children: [
        { path: '', component: PropertyBrowserComponent },
        { path: ':id', component: PropertyViewerComponent }
    ]},
    {path: 'crimeapi', component: CrimeapiComponent}
]

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }