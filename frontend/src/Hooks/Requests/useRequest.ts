import * as Api from '@/Api'
import {iApi} from '@/Api/Company/types';
import { getQueryKey } from '@/Utils/Query/getQueryKey';
import {useQuery} from '@tanstack/react-query'
import * as yup from 'yup';

export const queryKey = getQueryKey(['request'], (categories) => categories.USER);
export const useRequest = (params?: Partial<iApi.iGetRequest>) => {
    return useQuery({
        queryKey: [...queryKey, params],
        queryFn: async () => {
            try {
                const schema = yup.object({
                    application_id: yup.string().required()
                })
                const clearParams = await schema.validateSync(params)
                return Api.Company.getRequest(clearParams);
            } catch (ex) {
                return null
            }
        },
        staleTime: Infinity,
        gcTime: 0,
        enabled: Boolean(params)
    })
}