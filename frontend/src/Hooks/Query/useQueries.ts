import {useRouter} from './useRouter';
import {getQueries} from '@/Utils/Route/getQueries';

export const useQueries = <T>() => {
    const router = useRouter<T>();
    return getQueries<T>(router.asPath)
}


export default useQueries;