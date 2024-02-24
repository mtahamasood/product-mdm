import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { IProduct, IProductList } from '../../models/products';
import { take } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-products-list',
  templateUrl: './products-list.component.html',
  styleUrl: './products-list.component.scss',
})
export class ProductsListComponent implements OnInit {
  constructor(
    private apiService: ApiService,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}
  allProducts: IProduct[] = [];
  displayedColumns: string[] = ['productName', 'boxSize', 'action'];
  dataSource: IProduct[] = [];
  ngOnInit(): void {
    this.fetchAllProducts();
  }

  private fetchAllProducts(): void {
    this.apiService
      .getProducts()
      .pipe(take(1))
      .subscribe({
        next: (res: IProductList) => {
          if (res.statusCode === 200) {
            this.allProducts = res.data;
            this.dataSource = [...this.allProducts];
          }
        },
        error: (err) => {
          this.snackBar.open(
            'Connection error! Failed to fetch Products, Please try again!',
            'Ok',
            {
              duration: 2000,
            }
          );
        },
        complete: () => {},
      });
  }

  public createProductHandler(): void {
    this.router.navigate(['/products/create-product']);
  }

  public editProductHandler(productId: string): void {
    this.router.navigate([`/products/create-product/${productId}`]);
  }

  public deleteProductHandler(productId: string): void {
    this.apiService
      .deleteProduct(productId)
      .pipe(take(1))
      .subscribe({
        next: (res: IProductList) => {
          if (res.statusCode === 200) {
            this.snackBar.open('Product is deleted successfully', 'Ok', {
              duration: 2000,
            });
            this.allProducts = res.data;
            this.dataSource = [...this.allProducts];
          }
        },
        error: (err) => {
          this.snackBar.open(
            'Connection error! Failed to delete Products, Please try again!',
            'Ok',
            {
              duration: 2000,
            }
          );
        },
        complete: () => {},
      });
  }
}
