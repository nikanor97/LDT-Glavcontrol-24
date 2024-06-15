import {useRemainsStats as useRemainsStatsQuery} from '@/Hooks/Company/useRemainsStats';
import {usePrivateStore} from '../../../Store/Store';

export const useRemains = () => {
    const {quarter, year} = usePrivateStore((state) => state.remains);
    return useRemainsStatsQuery({quarter, year})
}