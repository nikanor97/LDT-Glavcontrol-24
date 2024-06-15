import * as Api from '@/Api'
import {iApi} from '@/Api/Company/types';
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query'

export const getKey = (params: iApi.iGetProcurements) => getQueryKey(['procurements', params], (categories) => categories.USER);
export const useProcurements = (params: iApi.iGetProcurements) => {
    return useQuery({
        queryKey: getKey(params),
        queryFn: () => Api.Company.getProcurements(params),
        staleTime: Infinity,
        gcTime: 20000
    })
}