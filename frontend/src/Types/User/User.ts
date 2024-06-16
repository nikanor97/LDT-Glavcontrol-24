

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
}