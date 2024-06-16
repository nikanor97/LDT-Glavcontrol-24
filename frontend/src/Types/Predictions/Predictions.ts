import {Products} from '../';

export type ID = string;
export type Item = {
    product: Products.Info;
    year: number;
    quarter: number;
    product_id: Products.ID;
    id: ID;
}