import * as Api from '@/Api';
import {iApi} from '@/Api/Company/types';
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query';

export const queryKey = (params: iApi.iGetRemainsStats) => getQueryKey(['companies', 'remains-stats', params], (category) => category.USER);
export const useRemainsStats = (params: iApi.iGetRemainsStats) => {
    return useQuery({
        queryKey: queryKey(params),
        queryFn: () => Api.Company.getRemainsStats(params),
        staleTime: Infinity,
        gcTime: 20000
    })
}