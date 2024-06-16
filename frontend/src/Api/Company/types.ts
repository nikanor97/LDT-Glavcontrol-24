import {Company, Procurement, Pagination, Remains, Requests, Products} from '@/Types';

export declare namespace iApi {
    type oGetMyCompany = Company.LegalInfo.Item
    type iGetProcurementsStats = {
        year: number;
        quarter: number;
    }
    type oGetProcurementsStats = Company.ProcurementsStats;
    type iGetRemainsStats = {
        year: number;
        quarter: number;
    }
    type oGetRemainsStats = Company.RemainsStats;
    type iGetProcurements = Pagination.Params;
    type oGetProcurements = {
        items: Procurement.Item[]
        pagination: Pagination.Info;
    }
    type iGetRemains = Pagination.Params;
    type oGetRemains = {
        items: Remains.Item[];
        pagination: Pagination.Info;
    }
    type iGetRequests = Pagination.Params;
    type oGetRequests = {
        items: Requests.Item[];
        pagination: Pagination.Info;
    }
    type iUploadProcurementsExcel = File|Blob;
    type oUploadProcurementsExcel = Procurement.Item[];
    type iGetCompanies = Pagination.Params;
    type oGetCompanies = {
        items: Company.ExistItem[];
        pagination: Pagination.Info;
    }
    type iCreateCompany = Company.Item;
    type oCreateCompany = Company.ExistItem;
    type iGetPrediction = Pagination.Params & {
        quarter: number;
        year: number;
    }
    type oGetPrediction = {
        items: Products.Product[];
        pagination: Pagination.Info;
    }
    type iGetRequest = {
        application_id: Requests.ID;
    }
    type oGetRequest = Requests.WithProduct;
    type iCreateRequest = Requests.CreateRequest;
    type oCreateRequest = Requests.WithProduct;
}