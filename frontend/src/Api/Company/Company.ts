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
    uploadRemainsExcel: (file: iApi.iUploadRemainsExcel) => {
        const fileData = new FormData();
        fileData.append("file", file);
        return axios.post<iApi.oUploadRemainsExcel>(
            paths.uploadRemainsExcel,
            fileData
        );
    },
    getCompanies: (params: iApi.iGetCompanies) => 
        axios.get<iApi.oGetCompanies>(paths.getCompanies, {params}),
    createCompany: (params: iApi.iCreateCompany) => 
        axios.post<iApi.oCreateCompany>(paths.createCompany, params),
    getPrediction: (params: iApi.iGetPrediction) => 
        axios.get<iApi.oGetPrediction>(paths.getPredictions, {params}),
    getRequest: (params: iApi.iGetRequest) => 
        axios.get<iApi.oGetRequest>(paths.getRequest, {params}),
    createRequest: (params: iApi.iCreateRequest) => 
        axios.post<iApi.oCreateRequest>(paths.createRequest, params),
    updateReqest: (params: iApi.iCreateRequest) => 
        axios.put<iApi.oCreateRequest>(paths.createRequest, params),
    createRequestFromPrediction: (params: iApi.iCreateRequestFromPrediction) => 
        axios.post<iApi.oCreateRequestFromPrediction>(paths.createRequestFromPredictions, params),
    updateCompany: (params: iApi.iUpdateCompany) =>
        axios.put<iApi.oUpdateCompany>(paths.updateCompany, params)

}