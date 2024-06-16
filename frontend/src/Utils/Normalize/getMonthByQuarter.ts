import {padStart} from 'lodash';


export const getMonthByQuarter = (quarter: number) => {
    const month = ((quarter - 1) * 3) + 1;
    return month;
}
