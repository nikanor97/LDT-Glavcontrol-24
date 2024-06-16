import { getMonthByQuarter } from "@/Utils/Normalize/getMonthByQuarter";
import dayjs from "dayjs";


export const useDateByQuarter = (quarter: number, year: number) => {
    const month = getMonthByQuarter(quarter);
    const date = dayjs(`${month}.02.${year}`, {format: 'MM.DD.YYYY'});
    return date
}
