import { QueryKey } from "@tanstack/react-query";


export enum QueryCategory {
    USER = 'USER',
    GLOBAL = 'GLOBAL',
    PAGE = 'PAGE'
}

export const getQueryKey = (
    key: QueryKey,
    getCategory: (category: typeof QueryCategory) => QueryCategory
): QueryKey => {
    const category = getCategory(QueryCategory);
    return [category, ...key]
}