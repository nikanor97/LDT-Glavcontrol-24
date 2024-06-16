

export declare namespace LegalInfo {
    export type ID = string;
    export type Item = {
        "id": ID;
        "created_at": string;
        "updated_at": string;
        "name": string;
        "region": string;
        "inn": string;
        "ogrn": string;
        "director": string;
        "foundation_date": string;
    }
}

export type ProcurementsStats = {
    "amount_contracts": number,
    "latest_contract_date": string;
    "contracts_stats": {
        "amount_contracts": number,
        "contracts_date": string;
    }[];
}

export type RemainsStats = {
    "saldo_begin_debet": number;
    "saldo_begin_credit": number;
    "saldo_period_debet": number;
    "saldo_period_credit": number;
    "saldo_end_debet": number;
    "saldo_end_credit": number;
}

export type ID = string;
export type Item = {
    "id": ID;
    "name": string;
    "region": string;
    "inn": string;
    "ogrn": string;
    "director": string;
    "foundation_date": string;
}

export type ExistItem = Item & {
    "created_at": string;
    "updated_at": string;
}