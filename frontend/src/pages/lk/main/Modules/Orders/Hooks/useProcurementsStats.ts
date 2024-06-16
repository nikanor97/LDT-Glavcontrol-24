import {usePrivateStore} from '../../../Store/Store';
import {useProcurementsStats} from '@/Hooks/Company/useProcurementsStats';

export const useProcuremtns = () => {
    const {quarter,year} = usePrivateStore((state) => state.orders);
    return useProcurementsStats({quarter, year});
}