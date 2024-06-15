import {QueryKey, useQuery} from '@tanstack/react-query';
import * as Api from '@/Api';
import { getQueryKey } from '@/Utils/Query/getQueryKey';



export const queryKey = getQueryKey(['me'], (category) => category.USER);
export const useUser = () => {
    return useQuery({
        queryKey,
        queryFn: Api.User.me,
        retry: false,
        staleTime: Infinity,
        refetchOnWindowFocus: false,
        refetchOnReconnect: false,
    })
}