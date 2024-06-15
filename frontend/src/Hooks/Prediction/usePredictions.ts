import { getQueryKey } from "@/Utils/Query/getQueryKey"
import {useQuery} from '@tanstack/react-query';
import * as Api from '@/Api';
import {iApi} from '@/Api/Company/types';

export const queryKey = getQueryKey(['predictions'], (categories) => categories.USER);
export const usePredictions = (params: iApi.iGetPrediction) => {
    return useQuery({
        queryKey: [...queryKey, params],
        queryFn: () => Api.Company.getPrediction(params),
        staleTime: Infinity,
        gcTime: 20000
    })
}