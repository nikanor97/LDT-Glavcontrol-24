export declare namespace SPGZ {
    type ID = string;
}


export type ID = string;
export type Info = {
    "name": "string",
    "price": number,
    "number": number,
    "amount": number
}
export type Product = {
    product: Info;
    year: number;
    quarter: number;
    product_id: ID;   
}
