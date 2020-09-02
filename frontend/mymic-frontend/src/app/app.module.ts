import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatTableModule} from '@angular/material/table';
import {MatTabsModule} from '@angular/material/tabs';
import {MatRadioModule} from '@angular/material/radio';
import {MatListModule} from '@angular/material/list';
import {MatButtonModule} from '@angular/material/button';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { MatPaginatorModule } from '@angular/material/paginator';
import {MatInputModule} from '@angular/material/input';
import {MatMenuModule} from '@angular/material/menu';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatIconModule} from '@angular/material/icon';

import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ScenarioTableComponent } from './scenario-table/scenario-table.component';

@NgModule({
  declarations: [
    AppComponent,
    ScenarioTableComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatTableModule,
    MatInputModule,
    MatTabsModule,
    MatRadioModule,
    MatListModule,
    MatMenuModule,
    MatButtonModule,
    MatPaginatorModule,
    MatIconModule,
    MatCheckboxModule,
    MatProgressBarModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
