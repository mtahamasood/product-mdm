import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import {
  IProduct,
  IProductDetailDTO,
  IProductList,
  IResponseDTO,
} from '../models/products';
import { PRODUCTSLIST } from '../../assets/data/products';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  headers = {
    'content-type': 'application/json',
  };
  baseUrl: string = environment.apiUrl;
  constructor(private http: HttpClient) {}

  createProduct(body: {
    ProductName: string;
    BoxSize: number;
  }): Observable<IResponseDTO> {
    //TODO replace below code with bottom commented code with live endpoint
    PRODUCTSLIST.push({ ProductId: crypto.randomUUID(), ...body });
    return of({ statusCode: 200, successMessage: 'success', error: null });
    // const url = `${this.baseUrl}/create-product`;
    // return this.http.post<any>(url, body, { headers: this.headers });
  }

  getProducts(): Observable<IProductList> {
    //TODO replace below code with bottom commented code with live endpoint
    return of({
      data: PRODUCTSLIST,
      statusCode: 200,
      successMessage: 'success',
      error: null,
    });
    // const url = `${this.baseUrl}/allProduct`;
    // return this.http.get<any>(url, { headers: this.headers });
  }

  updateProduct(body: IProduct): Observable<IResponseDTO> {
    const dIndex = PRODUCTSLIST.findIndex(
      (x: IProduct) => x.ProductId === body.ProductId
    );
    PRODUCTSLIST[dIndex] = body;
    return of({ statusCode: 200, successMessage: 'success', error: null });
    // const url = `${this.baseUrl}/product/${body.ProductId}`;
    // return this.http.post<any>(url, body, { headers: this.headers });
  }

  deleteProduct(productId: string): Observable<IProductList> {
    //TODO replace below code with bottom commented code with live endpoint
    const dIndex = PRODUCTSLIST.findIndex(
      (x: IProduct) => x.ProductId === productId
    );
    PRODUCTSLIST.splice(dIndex, 1);
    return of({
      data: PRODUCTSLIST,
      statusCode: 200,
      successMessage: 'success',
      error: null,
    });
    // const url = `${this.baseUrl}/product/${productId}`;
    // return this.http.delete<any>(url, { headers: this.headers });
  }

  fetchSingleProductDetails(productId: string): Observable<IProductDetailDTO> {
    //TODO replace below code with bottom commented code with live endpoint
    const productDetail = PRODUCTSLIST.find(
      (x: IProduct) => x.ProductId === productId
    );

    const defaultProduct: IProduct = {
      ProductId: '',
      ProductName: '',
      BoxSize: 0,
    };
    return of({
      data: productDetail ? productDetail : defaultProduct,
      statusCode: 200,
      successMessage: 'success',
      error: null,
    });
    // const url = `${this.baseUrl}/product/${productId}`;
    // return this.http.get<IProductDetailDTO>(url, { headers: this.headers });
  }
}
