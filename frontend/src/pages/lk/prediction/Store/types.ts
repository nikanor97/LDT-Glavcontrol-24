import {iApi} from '@/Api/Company/types';
import {Predictions} from '@/Types'

export type iState = {
    params: iApi.iGetPrediction;
    selected: Predictions.ID[];

}

export type iActions = {
    changeParams: (params: Partial<iState['params']>) => any;
    setSelected: (values: Predictions.ID[]) => any;

}