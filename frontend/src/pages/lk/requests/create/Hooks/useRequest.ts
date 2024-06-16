import {useRequest as useRequestQuery} from '@/Hooks/Requests/useRequest';
import {useQueries} from '@/Hooks/Query/useQueries';
import {iQueries} from '../types';

export const useRequest = () => {
    const queries = useQueries<iQueries>();
    return useRequestQuery({
        application_id: queries.id
    });
}

export default useRequest;