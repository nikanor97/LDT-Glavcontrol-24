import {isAxiosError, AxiosResponse} from 'axios';
import {Api} from '@/Types';


export const getErrorMessage = (ex: unknown) => {
    const messages = {
        front: {
            default: 'Ошибка при выполнении запроса',
            entityTooLarge: 'Объект запроса слишком велик'
        },
        back: 'Ошибка при получении ответа от сервера'
    }
    let response:AxiosResponse|undefined;

    //Если апи вернуло http ошибку
    if (isAxiosError(ex)) {
        response = ex.response;
    }
    //Если ошибка из интерсептора
    if (Api.Guard.isAxiosResponse(ex)) {
        response = ex;
    }

    //exeption - не из-за запроса
    if (!response) return messages.front.default;
    if (response.status === 413) {
        return messages.front.entityTooLarge;
    }
    //Далее http код 200 + какой то респонс
    if (Api.Guard.isBadResponse(response)) {
        const {data} = response;
        return data.error;
    }
    return messages.front.default;
}