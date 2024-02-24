import { Component, OnInit } from '@angular/core';
import {
  UntypedFormBuilder,
  UntypedFormGroup,
  Validators,
} from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { take } from 'rxjs';
import { IProductDetailDTO, IResponseDTO } from '../../models/products';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-create-product',
  templateUrl: './create-product.component.html',
  styleUrl: './create-product.component.scss',
})
export class CreateProductComponent implements OnInit {
  productForm!: UntypedFormGroup;
  productId!: string;
  updateProductMode: boolean = false;
  constructor(
    private fb: UntypedFormBuilder,
    private apiService: ApiService,
    private snackBar: MatSnackBar,
    private router: Router,
    private activatedRoute: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.formBuilderHandler();
    this.getParams();
  }

  private formBuilderHandler(): void {
    this.productForm = this.fb.group({
      ProductName: [null, Validators.required],
      BoxSize: [null, Validators.required],
    });
  }

  private getParams() {
    this.activatedRoute.params.pipe(take(1)).subscribe((params) => {
      this.productId = params['id'];
      if (this.productId) {
        this.updateProductMode = true;
        this.fetchProductDetailsHandler(this.productId);
      }
    });
  }

  public saveProductHandler(): void {
    if (this.productForm.invalid) {
      return;
    }
    if (this.updateProductMode) {
      this.updateProductHandler();
      return;
    }
    const payLoad: {
      ProductName: string;
      BoxSize: number;
    } = this.productForm.value;

    this.apiService
      .createProduct(payLoad)
      .pipe(take(1))
      .subscribe({
        next: (res: IResponseDTO) => {
          if (res.statusCode === 200) {
            this.snackBar.open('Product Created Sucessfully', 'Ok', {
              duration: 2000,
            });
            this.router.navigate(['']);
          }
        },
        error: (err) => {
          this.snackBar.open(
            'Connection error! Failed to create product, Please try again!',
            'Ok',
            {
              duration: 2000,
            }
          );
        },
        complete: () => {},
      });
  }

  private updateProductHandler(): void {
    const payLoad: {
      ProductName: string;
      BoxSize: number;
      ProductId: string;
    } = { ProductId: this.productId, ...this.productForm.value };

    this.apiService
      .updateProduct(payLoad)
      .pipe(take(1))
      .subscribe({
        next: (res: IResponseDTO) => {
          if (res.statusCode === 200) {
            this.snackBar.open('Product Updated Sucessfully', 'Ok', {
              duration: 2000,
            });
            this.router.navigate(['']);
          }
        },
        error: (err) => {
          this.snackBar.open(
            'Connection error! Failed to update product, Please try again!',
            'Ok',
            {
              duration: 2000,
            }
          );
        },
        complete: () => {},
      });
  }

  private fetchProductDetailsHandler(productId: string): void {
    this.apiService
      .fetchSingleProductDetails(productId)
      .pipe(take(1))
      .subscribe({
        next: (res: IProductDetailDTO) => {
          if (res.statusCode === 200) {
            this.productForm.patchValue(res.data);
          }
        },
        error: (err) => {
          this.snackBar.open(
            'Connection error! Failed to fetch Product details, Please try again!',
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
