import {Requests, User} from '@/Types';
import qs from 'qs';

export const Routes = {
    api: {
        ordersExportExcel: (userId: User.Id) => {
            const query = qs.stringify({
                user_id: userId
            }, {
                addQueryPrefix: true,
            })
            return `/api/v1/projects/procurements-export-excel${query}`
        },
        predictionsExportExcel: (year: number, userId: User.Id, quarter?: number) => {
            const query = qs.stringify({
                user_id: userId,
                quarter,
                year
            }, {
                addQueryPrefix: true,
            })
            return `/api/v1/projects/forecast-export-excel${query}`
        },
        predictionsExportJSON: (year: number, userId: User.Id, quarter?: number) => {
            const query = qs.stringify({
                user_id: userId,
                quarter,
                year
            }, {
                addQueryPrefix: true,
            })
            return `/api/v1/projects/forecast-json-full${query}`
        },
        remainsExportExcel: (userId: User.Id) => {
            const query = qs.stringify({
                user_id: userId,
            }, {
                addQueryPrefix: true,
            })
            return `/api/v1/projects/remains-export-excel${query}`
        }
    },
    login: '/login',
    gateway: '/',
    lk: {
        main: '/lk',
        orders: '/lk/orders',
        prediction: '/lk/prediction',
        remains: '/lk/remains',
        requests: (ids?: Requests.ID[]) => {
            const query = qs.stringify({ids}, {
                addQueryPrefix: true,
            })
            return '/lk/requests' + query;
        },
        createRequest: (id?: Requests.ID) => {
            const query = qs.stringify({id}, {
                addQueryPrefix: true,
            })
            return '/lk/requests/create' + query;
        }
    },
    lkAdmin: {
        main: '/lk-admin',
        companies: '/lk-admin/companies',
        users: '/lk-admin/users',
    }
}


export default Routes;