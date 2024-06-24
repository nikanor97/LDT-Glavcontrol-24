import axios from '../Request';
import paths from './paths';
import {iApi} from './types';
import CS from '@/Storages/Cookie';

export default {
    me: async () => {
        try {
            if (!CS.token.getAccess()) return null;
            if (!CS.token.getRefresh()) return null;
            return await axios.get<iApi.oMe>(paths.me);
        } catch (ex) {
            return null;
        }
    },
    getAllUsers: () => 
        axios.get<iApi.oGetAllUsers>(paths.getAllUsers),
    getUsersWithCompany: (params: iApi.iGetUsersWithCompany) => 
        axios.get<iApi.oGetUsersWithCompany>(paths.getUsersWithCompany, {params}),
}