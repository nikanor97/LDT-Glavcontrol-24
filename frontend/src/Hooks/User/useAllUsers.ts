import * as Api from '@/Api'
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query'

export const getKey = getQueryKey(['users', 'all'], (categories) => categories.USER);
export const useAllUsers = () => {
    return useQuery({
        queryKey: getKey,
        queryFn: () => Api.User.getAllUsers(),
        staleTime: Infinity,
        gcTime: 20000
    })
}