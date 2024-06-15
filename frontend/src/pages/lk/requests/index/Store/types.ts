import {Pagination} from '@/Types';

export type iState = {
    params: Pagination.Params;
}

export type iActions = {
    changeParams: (params: Partial<iState['params']>) => any;
}