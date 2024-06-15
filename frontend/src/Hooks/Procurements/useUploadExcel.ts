import * as Api from '@/Api';
import {useMutation} from '@tanstack/react-query';
import {iApi} from '@/Api/Company/types';



export const useUploadExcel = () => {
    return useMutation({
        mutationFn: (params: iApi.iUploadProcurementsExcel) => {
            return Api.Company.uploadProcurementsExcel(params)
        }
    })  
}