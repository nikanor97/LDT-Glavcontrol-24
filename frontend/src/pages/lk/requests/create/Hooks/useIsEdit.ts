import useQueries from '@/Hooks/Query/useQueries';
import {iQueries} from '../types';



export const useIsEdit = () => {
    const queries = useQueries<iQueries>();
    return Boolean(queries.id);
}