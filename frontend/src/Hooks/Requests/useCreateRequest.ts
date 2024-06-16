import {useMutation} from '@tanstack/react-query';
import {iApi} from '@/Api/Company/types';
import * as Api from '@/Api';


export const mutationKey = ['requests','create'];
export const useCreateRequest = () => {
    return useMutation({
        mutationKey,
        mutationFn: (params: iApi.iCreateRequest) => {
            return Api.Company.createRequest(params);
        },
    })
}