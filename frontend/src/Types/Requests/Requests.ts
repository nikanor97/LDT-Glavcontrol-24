import {Products} from '../';

export type ID = string;
export type Item = {
    "id": ID;
    "created_at": string;
    "updated_at": string;
    "spgz_id": Products.SPGZ.ID;
    "spgz_name": string;
    "procurement_date": string;
    "price": number;
    "way_to_define_supplier": string;
    "contract_basis": string;
}