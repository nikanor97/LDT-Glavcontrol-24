import {User, Pagination} from '@/Types';

export declare namespace iApi {
    type oMe = User.Item;
    type oGetAllUsers = User.Item[];
    type oGetUsersWithCompany = {
        items: User.WithCompany[];
        pagination: Pagination.Info;
    };
    type iGetUsersWithCompany = Pagination.Params;
}