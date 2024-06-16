import {useMutation} from '@tanstack/react-query';
import {iApi} from '@/Api/Company/types';
import * as Api from '@/Api';


export const mutationKey = ['requests','update']
export const useUpdateRequest = () => {
    return useMutation({
        mutationKey,
        mutationFn: (params: iApi.iCreateRequest) => {
            return Api.Company.updateReqest(params);
        },
    })
}