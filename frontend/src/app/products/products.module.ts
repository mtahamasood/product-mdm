import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductsListComponent } from './products-list/products-list.component';
import { RouterModule, Routes } from '@angular/router';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { CreateProductComponent } from './create-product/create-product.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';

export const routes: Routes = [
  { path: '', component: ProductsListComponent, pathMatch: 'full' },
  {
    path: 'create-product',
    component: CreateProductComponent,
  },
  {
    path: 'create-product/:id',
    component: CreateProductComponent,
  },
];

@NgModule({
  declarations: [ProductsListComponent, CreateProductComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    MatSnackBarModule,
    MatTableModule,
    MatIconModule,
    MatButtonModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
  ],
})
export class ProductsModule {}
