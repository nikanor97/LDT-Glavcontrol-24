import {useMutation} from '@tanstack/react-query';
import {iApi} from '@/Api/Company/types';
import {message} from 'antd';
import {useRouter} from 'next/router';
import getRoute from '@/Routes/Routes'
import * as Api from '@/Api';


export const mutationKey = ['requests','create', 'by-predictions'];
export const useCreateRequestByPredicitions = () => {
    const router = useRouter();
    return useMutation({
        mutationKey,
        mutationFn: (params: iApi.iCreateRequestFromPrediction) => {
            return Api.Company.createRequestFromPrediction(params);
        },
        onSuccess: (data) => {
            const {application_ids} = data;
            if (application_ids.length === 0) {
                message.error('К сожалению, нам не удалось создать заявки по выбранным прогнозам');
                return
            }
            if (application_ids.length === 1) {
                router.push(getRoute.lk.createRequest(application_ids[0]))
                return;
            }
            if (application_ids.length > 1) {
                router.push(getRoute.lk.requests(application_ids))
                return;
            }
        }
    })
}