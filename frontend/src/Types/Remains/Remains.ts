

export type ID = string;
export type Item = {
    "id": string;
    "created_at": string;
    "updated_at": string;
    "cmo": string;
    "koc": number,
    "number": number,
    "indicator": number,
    "saldo_begin_debet": number,
    "saldo_begin_credit": number,
    "saldo_period_debet": number,
    "saldo_period_credit": number,
    "saldo_end_debet": number,
    "saldo_end_credit": number,
    "product_id": string;
}