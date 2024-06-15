


import {useMutation, useMutationState} from '@tanstack/react-query';
import {iApi} from '@/Api/Company/types';
import * as Api from '@/Api';
import { useFirstMutation } from '../Query/useFirstMutation';


export const mutationKey = ['comapnies','create'];
export const useCreateCompanyState = () => {
    const mutations = useMutationState({
        filters: {
            mutationKey,
        }
    })
    return useFirstMutation(mutations);
}
export const useCreateCompany = () => {
    return useMutation({
        mutationKey,
        mutationFn: (params: iApi.iCreateCompany) => {
            return Api.Company.createCompany(params)
        },
    })
}