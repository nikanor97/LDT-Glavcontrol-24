import {iApi} from '@/Api/Company/types';

export type iState = {
    params: iApi.iGetPrediction;
}

export type iActions = {
    changeParams: (params: Partial<iState['params']>) => any;
}