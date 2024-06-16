import * as Api from '@/Api'
import {iApi} from '@/Api/Company/types';
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query'

export const queryKey = getQueryKey(['procurements'], (categories) => categories.USER);
export const useProcurements = (params: iApi.iGetProcurements) => {
    return useQuery({
        queryKey: [...queryKey, params],
        queryFn: () => Api.Company.getProcurements(params),
        staleTime: Infinity,
        gcTime: 20000
    })
}