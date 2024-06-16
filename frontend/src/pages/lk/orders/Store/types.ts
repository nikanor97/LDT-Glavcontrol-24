import {Pagination, Procurement} from '@/Types';

export type iState = {
    params: Pagination.Params;
    selected: Procurement.ID[];
}

export type iActions = {
    changeParams: (params: Partial<iState['params']>) => any;
    setSelected: (values: Procurement.ID[]) => any;
}