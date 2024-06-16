import axios from '../Request';
import paths from './paths';
import {iApi} from './types';

export default {
    login: (params: iApi.iLogin) => {
        return axios.post<iApi.oLogin>(paths.login, params)
    },
    registration: (params: iApi.iRegistration) => {
        return axios.post(paths.registration, {
            ...params,
            is_deleted: false,
        });
    }
}