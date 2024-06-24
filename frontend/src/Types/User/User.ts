import { Company } from "..";


export declare namespace Role {
    export type BaseRole = 
        'user' |
        'admin';

    //Выделили состояние без логина в отдельное значение чтобы проще было указывать у страниц в массиве
    export type State = 
        'auth' |
        'unauth';

    export type Result = BaseRole | State;

    export type ResultValues = Record<Result, boolean>;
}


export type Token = {
    access_token: string,
    refresh_token: string,
    token_type: string,
    access_expires_at: number;
    refresh_expires_at: number
}

export type Id = string;
export type Item = {
    id: Id;
    created_at: string;
    updated_at: string;
    name: string,
    permission_create_order: boolean;
    permission_read_stat: boolean;
    email: string,
    role: Role.BaseRole;
    telegram_username?: string;
}

export type RegUser = Omit<Item, 'created_at' | 'updated_at'> & {
    company_id: Company.ID
};

export type WithCompany = {
    "user_id": Id;
    "user_name": string;
    "user_email": "string",
    "user_permission_read_stat": boolean;
    "user_permission_create_order": boolean;
    "user_is_deleted": boolean;
    "user_role": Role.BaseRole;
    "user_telegram_username"?: string;
    "company_id": Company.ID;
    "company_name": string;
    "company_region": string;
    "company_inn": string;
    "company_ogrn": string;
    "company_director": string;
    "company_foundation_date": string;
}