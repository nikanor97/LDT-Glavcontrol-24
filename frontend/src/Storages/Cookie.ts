import cookies from 'js-cookie';
import dayjs from 'dayjs';

const convertToDays = (secounds: number) => {
    return secounds / 60 / 60 / 24;
}

const results = {
    token: (() => {
        const ACCESS_TOKEN = 'gcl_access_token'
        const REFRESH_TOKEN = 'gcl_refresh_token'
        const ACCESS_UNTIL = 'gcl_access_until'
        const REFRESH_UNTIL = 'gcl_refresh_until'
        
        return {
            getAccess: () => {
                const token = cookies.get(ACCESS_TOKEN);
                const until = cookies.get(ACCESS_UNTIL);
                if (!token) return null;
                return {
                    token,
                    until: until ? dayjs(until) : null
                }
            },
            getRefresh: () => {
                const token = cookies.get(REFRESH_TOKEN);
                const until = cookies.get(REFRESH_UNTIL);
                if (!token) return null;
                return {
                    token,
                    until: until ? dayjs(until) : null
                }
            },
            setAccess: (token: string, expiredSec: number) => {
                const until = dayjs()
                    .add(expiredSec, 'seconds')
                    .toISOString()
                cookies.set(ACCESS_TOKEN, token, {expires: convertToDays(expiredSec)})
                cookies.set(ACCESS_UNTIL, until, {expires: convertToDays(expiredSec)})
            },
            setRefresh: (token: string, expiredSec: number) => {
                const until = dayjs()
                    .add(expiredSec, 'seconds')
                    .toISOString()
            
                cookies.set(REFRESH_TOKEN, token, {expires: convertToDays(expiredSec)})
                cookies.set(REFRESH_UNTIL, until, {expires: convertToDays(expiredSec)})
            },
            clear: () => {
                cookies.remove(ACCESS_TOKEN);
                cookies.remove(ACCESS_UNTIL);
                cookies.remove(REFRESH_TOKEN);
                cookies.remove(REFRESH_UNTIL);
            }
        }
    })()
}

export default results;