import {useMutation, useMutationState} from '@tanstack/react-query';
import {iApi} from '@/Api/Auth/types';
import * as Api from '@/Api';
import { useFirstMutation } from '../Query/useFirstMutation';


export const mutationKey = ['auth','registration'];
export const useRegistrationState = () => {
    const mutations = useMutationState({
        filters: {
            mutationKey,
        }
    })
    return useFirstMutation(mutations);
}
export const useRegistration = () => {
    return useMutation({
        mutationKey,
        mutationFn: (params: iApi.iRegistration) => {
            return Api.Auth.registration(params);
        },
    })
}