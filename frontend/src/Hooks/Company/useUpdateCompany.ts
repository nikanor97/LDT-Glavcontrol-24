


import {useMutation, useMutationState} from '@tanstack/react-query';
import {iApi} from '@/Api/Company/types';
import * as Api from '@/Api';
import { useFirstMutation } from '../Query/useFirstMutation';


export const mutationKey = ['comapnies','update'];
export const useUpdateCompanyState = () => {
    const mutations = useMutationState({
        filters: {
            mutationKey,
        }
    })
    return useFirstMutation(mutations);
}
export const useUpdateCompany = () => {
    return useMutation({
        mutationKey,
        mutationFn: (params: iApi.iUpdateCompany) => {
            return Api.Company.updateCompany(params)
        },
    })
}