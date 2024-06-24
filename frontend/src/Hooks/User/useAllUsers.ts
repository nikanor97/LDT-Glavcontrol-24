import * as Api from '@/Api'
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query'
import {iApi} from '@/Api/User/types';

export const getKey = getQueryKey(['users', 'all'], (categories) => categories.USER);
export const useAllUsers = (params: iApi.iGetUsersWithCompany) => {
    return useQuery({
        queryKey: [...getKey, params],
        queryFn: () => Api.User.getUsersWithCompany(params),
        staleTime: Infinity,
        gcTime: 20000
    })
}