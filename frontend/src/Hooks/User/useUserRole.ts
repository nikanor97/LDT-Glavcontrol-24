import {User} from '@/Types';
import {useUser} from './useUser';

export const useUserRole = ():User.Role.ResultValues => {
    const {data, isFetched} = useUser();
    const result: User.Role.ResultValues = {
        admin: false,
        auth: false,
        user: false,
        unauth: true
    }
    //Данные еще не были запрошены точно неавторизованы
    if (!isFetched) return result;
    //Для неавторизованного пользователя, но данные уже загружены
    if (!data) return result;
    //Данные есть значит мы авторизованы
    result.unauth = false;
    result.auth = true;
    if (data.role === 'user') {
        result.user = true;
    } else {
        result.admin = true;
    }
    return result;
}