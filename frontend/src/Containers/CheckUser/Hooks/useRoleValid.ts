import { useUserRole } from "@/Hooks/User/useUserRole"
import {App} from '@/Types';
import {isArray} from 'lodash';

type PageRole = App.Next.NextPage['Role'];

export const useRoleValid = (pageRole: PageRole) => {
    const userRole = useUserRole();
    if (!pageRole) return true;
    if (isArray(pageRole)) {
        const values = pageRole.map((targetRole) => userRole[targetRole]);
        return values.some(Boolean);
    }
    return pageRole(userRole);
}