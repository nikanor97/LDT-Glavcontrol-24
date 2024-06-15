import * as Api from '@/Api'
import {iApi} from '@/Api/Company/types';
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query'

export const queryKey = getQueryKey(['companies'], (categories) => categories.USER);
export const useCompanies = (params: iApi.iGetRemains) => {
    return useQuery({
        queryKey: [...queryKey, params],
        queryFn: () => Api.Company.getCompanies(params),
        staleTime: Infinity,
        gcTime: 20000,
    })
}