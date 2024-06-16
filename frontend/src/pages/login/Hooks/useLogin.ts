import {useMutation} from '@tanstack/react-query';
import {iApi} from '@/Api/Auth/types';
import * as Api from '@/Api';
import CS from '@/Storages/Cookie';

export const useLogin = () => {
    return useMutation({
        mutationFn: (params: iApi.iLogin) => {
            return Api.Auth.login(params);
        },
        onSuccess: (data) => {
            CS.token.setAccess(data.access_token, data.access_expires_at);
            CS.token.setRefresh(data.refresh_token, data.refresh_expires_at);
        }
    })
}