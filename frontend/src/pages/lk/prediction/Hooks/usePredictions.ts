import {usePredictions as usePredictionsQuery} from '@/Hooks/Prediction/usePredictions';
import {usePrivateStore} from '../Store/Store';

export const usePredictions = () => {
    const params = usePrivateStore((state) => state.params);
    return usePredictionsQuery(params);
}

export default usePredictions;