import {iApi} from '@/Api/User/types';

export type iState = {
    createUser: {
        visible: boolean;
    }
    usersListParams: iApi.iGetUsersWithCompany;
}

export type iActions = {
    openDrawer: () => any;
    closeDrawer: () => any;
    changeParams: (params: Partial<iApi.iGetUsersWithCompany>) => any;
}