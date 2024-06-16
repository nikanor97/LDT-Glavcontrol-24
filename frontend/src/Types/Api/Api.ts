import {AxiosResponse} from 'axios';
import * as yup from 'yup';

export type SuccessResponse<T> = {
    data: T;
    error: null,
    error_metadata: null,
    status_code: 200
}


export type BadResponse<T> = {
    data: null,
    error: string
    error_metadata: T,
    status_code: 404 | 500
}


export type Response<S,B> = 
    SuccessResponse<S> |
    BadResponse<B>;


export const Guard = {
    isBadResponse: <T>(item: any): item is AxiosResponse<BadResponse<T>> => {
        const schema = yup.object({
            status: yup.number()
                .required()
                .equals([200]),
            data: yup.object({
                status_code: yup.number()
                    .required()
                    .notOneOf([200])
            })
        })

        try {
            return schema.validateSync(item) ? true : false;
        } catch (ex) {
            return false;
        }
    },
    isAxiosResponse: (item: any): item is AxiosResponse => {
        const schema = yup.object({
            data: yup.object().required(),
            status: yup.number().required(),
            statusText: yup.string().required(),
            config: yup.object().required(),
        })
        try {
            return schema.validateSync(item) ? true : false;
        } catch (ex) {
            return false;
        }     
    }
}