export interface IProduct {
  ProductId: string;
  ProductName: string;
  BoxSize: number;
}

export interface IResponseDTO {
  error: null | string;
  statusCode: number;
  successMessage: string;
}

export interface IProductList extends IResponseDTO {
  data: IProduct[];
}

export interface IProductDetailDTO extends IResponseDTO {
  data: IProduct;
}
