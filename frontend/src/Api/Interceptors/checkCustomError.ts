import { AxiosResponse } from "axios";
import {Api} from '@/Types';


export const checkCustomError = (response: AxiosResponse) => {
    //Проверяем все респонсы на ошибки
    if (Api.Guard.isBadResponse(response)) {
        return Promise.reject(response)
    }
    return response;
}