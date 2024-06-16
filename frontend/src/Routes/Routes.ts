import {Requests} from '@/Types';
import qs from 'qs';

export const Routes = {
    login: '/login',
    gateway: '/',
    lk: {
        main: '/lk',
        orders: '/lk/orders',
        prediction: '/lk/prediction',
        remains: '/lk/remains',
        requests: '/lk/requests',
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