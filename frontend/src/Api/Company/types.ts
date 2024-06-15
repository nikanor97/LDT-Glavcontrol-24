import {Company, Procurement, Pagination, Remains, Requests} from '@/Types';

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

}