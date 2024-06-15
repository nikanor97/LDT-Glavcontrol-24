import paths from './path';
import axios from '../Request';
import {iApi} from './types';

export default {
    getMyCompany: () => 
        axios.get<iApi.oGetMyCompany>(paths.getMyCompany),
    getProcurementsStats: (params:iApi.iGetProcurementsStats) =>
        axios.get<iApi.oGetProcurementsStats>(paths.getProcurementsStats, {params}),
    getRemainsStats: (params:iApi.iGetRemainsStats) =>
        axios.get<iApi.oGetRemainsStats>(paths.getRemainsStats, {params}),
    getProcurements: (params: iApi.iGetProcurements) => 
        axios.get<iApi.oGetProcurements>(paths.getProcurements, {params}),
    getRemains: (params: iApi.iGetRemains) => 
        axios.get<iApi.oGetRemains>(paths.getRemains, {params}),
    getRequests: (params: iApi.iGetRequests) => 
        axios.get<iApi.oGetRequests>(paths.getRequests, {params}),
    uploadProcurementsExcel: (file: iApi.iUploadProcurementsExcel) => {
        const fileData = new FormData();
        fileData.append("file", file);
        return axios.post<iApi.oUploadProcurementsExcel>(
            paths.uploadProcurementsExcel,
            fileData
        );
    },
    getCompanies: (params: iApi.iGetCompanies) => 
        axios.get<iApi.oGetCompanies>(paths.getCompanies, {params}),
    createCompany: (params: iApi.iCreateCompany) => 
        axios.post<iApi.oCreateCompany>(paths.createCompany, params),


}