import * as Api from '@/Api';
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query';


export const queryKey = getQueryKey(['companies','my-company'], (category) => category.USER);
export const useMyCompany = () => {
    return useQuery({
        queryKey,
        queryFn: Api.Company.getMyCompany,
        staleTime: Infinity,
        gcTime: Infinity
    })
}