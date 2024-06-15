import * as Api from '@/Api'
import {iApi} from '@/Api/Company/types';
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query'

export const getKey = (params: iApi.iGetRemains) => getQueryKey(['remains', params], (categories) => categories.USER);
export const useRemains = (params: iApi.iGetRemains) => {
    return useQuery({
        queryKey: getKey(params),
        queryFn: () => Api.Company.getRemains(params),
        staleTime: Infinity,
        gcTime: 20000
    })
}