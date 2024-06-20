import * as Api from '@/Api'
import {iApi} from '@/Api/Company/types';
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query'

export const getKey = (params: iApi.iGetRequests) => getQueryKey(['requests', params], (categories) => categories.USER);
export const useRequests = (params: iApi.iGetRequests) => {
    return useQuery({
        queryKey: getKey(params),
        queryFn: () => Api.Company.getRequests(params),
        staleTime: Infinity,
        gcTime: 0
    })
}