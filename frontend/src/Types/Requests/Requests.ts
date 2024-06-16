import {Products, User} from '../';

export type Status = 'draft' | 'ready'
export type ID = string;
export type Item = {
    "id": ID;
    "created_at": string;
    "updated_at": string;
    "calculation_id": string;
    "lot_id": string;
    "client_id": string;
    "shipment_start_date": string;
    "shipment_end_date": string;
    "shipment_volume": 0,
    "shipment_address": string;
    "shipment_terms": string;
    "year": 0,
    "gar_id": string;
    "spgz_end_id": string;
    "amount": 0,
    "unit_of_measurement": string;
    "author_id": User.Id;
    "status": Status;
}

export type WithProduct = Item & {
    products: Product[];
}

export type Product = Products.Info & {
    "id": Products.ID;
    "created_at": string;
    "updated_at": string;
}

export type CreateRequest = Omit<Item, 'created_at' | 'updated_at'> & {
    products: (Product | Products.Info)[]
}