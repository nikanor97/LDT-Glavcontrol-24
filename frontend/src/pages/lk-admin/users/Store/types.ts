import {iApi} from '@/Api/User/types';
import { User } from '@/Types';

export type iState = {
    editUser: {
        visible: boolean;
        item: User.WithCompany | null;
    },
    createUser: {
        visible: boolean;
    }
    usersListParams: iApi.iGetUsersWithCompany;
}

export type iActions = {
    openDrawer: () => any;
    closeDrawer: () => any;
    changeParams: (params: Partial<iApi.iGetUsersWithCompany>) => any;
    openEditModal: (item: User.WithCompany) => any;
    closeEditModal: () => any;
}