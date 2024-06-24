import {useMutation} from '@tanstack/react-query';
import {iApi} from '@/Api/Auth/types';
import * as Api from '@/Api';


export const mutationKey = ['auth','saveUser'];
export const useSaveUser = () => {
    return useMutation({
        mutationKey,
        mutationFn: (params: iApi.iSaveUser) => {
            return Api.Auth.saveUser(params);
        },
    })
}