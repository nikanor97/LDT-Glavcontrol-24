import {Pagination} from '@/Types';


export type iState = {
    params: Pagination.Params;
    addCompany: {
        visible: boolean;
    }
}

export type iActions = {
    changeParams: (params: Partial<iState['params']>) => any;
    closeDrawer: () => any;
    openDrawer: () => any;
}