import {Pagination, Requests} from '@/Types';

export type iState = {
    params: Pagination.Params;
    deleteModal: {
        visible: boolean;
        item: Requests.Item | null;
    }
}

export type iActions = {
    changeParams: (params: Partial<iState['params']>) => any;
    openDeleteModal: (item: Requests.Item) => any;
    closeDeleteModal: () => any;
}