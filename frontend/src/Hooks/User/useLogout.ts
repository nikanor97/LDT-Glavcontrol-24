
import {useQueryClient} from '@tanstack/react-query';
import {queryKey as userQueryKey} from '@/Hooks/User/useUser';
import {QueryCategory} from '@/Utils/Query/getQueryKey';
import CS from '@/Storages/Cookie';


export const useLogout = () => {
    const client = useQueryClient();
    return () => {
        CS.token.clear();
        client.resetQueries({queryKey: [QueryCategory.USER]});
    }

}