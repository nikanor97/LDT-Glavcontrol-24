import * as Api from '@/Api';
import {iApi} from '@/Api/Company/types';
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query';

export const queryKey = (params: iApi.iGetProcurementsStats) => getQueryKey(['companies', 'procurements-stats', params], (category) => category.USER);
export const useProcurementsStats = (params: iApi.iGetProcurementsStats) => {
    return useQuery({
        queryKey: queryKey(params),
        queryFn: () => Api.Company.getProcurementsStats(params),
        staleTime: Infinity,
        gcTime: 20000
    })
}