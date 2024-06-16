import {Company, Pagination} from '@/Types';


export type iState = {
    params: Pagination.Params;
    addCompany: {
        visible: boolean;
        item: Company.ExistItem | null;
    }
}

export type iActions = {
    changeParams: (params: Partial<iState['params']>) => any;
    closeDrawer: () => any;
    openDrawer: (item?: Company.ExistItem) => any;
}