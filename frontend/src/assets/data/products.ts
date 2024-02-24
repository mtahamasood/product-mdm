import { IProduct } from '../../app/models/products';

export let PRODUCTSLIST: IProduct[] = [
  {
    ProductId: crypto.randomUUID(),
    ProductName: 'Test Product 1',
    BoxSize: 10,
  },
  {
    ProductId: crypto.randomUUID(),
    ProductName: 'Test Product 2',
    BoxSize: 12,
  },
  {
    ProductId: crypto.randomUUID(),
    ProductName: 'Test Product 3',
    BoxSize: 20,
  },
  {
    ProductId: crypto.randomUUID(),
    ProductName: 'Test Product 4',
    BoxSize: 30,
  },
  {
    ProductId: crypto.randomUUID(),
    ProductName: 'Test Product 5',
    BoxSize: 40,
  },
  {
    ProductId: crypto.randomUUID(),
    ProductName: 'Test Product 6',
    BoxSize: 50,
  },
];
