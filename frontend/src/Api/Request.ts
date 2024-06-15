import Axios from 'axios';
import Qs from 'qs';
import {checkCustomError} from './Interceptors/checkCustomError';
import {setAuthHeader} from './Interceptors/setAuthHeader';
import {Api} from '@/Types';

const axios = Axios.create({
    baseURL: '/api',
    paramsSerializer: (params) => Qs.stringify(params, {arrayFormat: 'repeat'})
});

axios.interceptors.request.use(setAuthHeader);
axios.interceptors.response.use(checkCustomError);


export default {
    ...axios,
    get: <T>(...args: Parameters<typeof axios.get>) => {
        return axios.get<Api.SuccessResponse<T>>(...args)
            .then((response) => response.data.data)
    },
    post: async <T>(...args: Parameters<typeof axios.post>) => {
        return axios.post<Api.SuccessResponse<T>>(...args)
            .then((response) => response.data.data)
    },
    patch: async <T>(...args: Parameters<typeof axios.patch>) => {
        const response = await axios.patch<Api.SuccessResponse<T>>(...args);
        return response.data.data;
    },
    delete: async <T>(...args: Parameters<typeof axios.delete>) => {
        const response = await axios.delete<Api.SuccessResponse<T>>(...args);
        return response.data.data;
    },
}





