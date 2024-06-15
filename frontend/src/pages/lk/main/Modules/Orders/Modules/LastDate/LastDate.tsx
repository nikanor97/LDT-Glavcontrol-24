import {useMemo} from 'react';
import StatisticItem from "../../Components/StatsticItem/StatisticItem";
import { HiClipboardDocumentCheck } from "react-icons/hi2";
import {useProcuremtns} from '../../Hooks/useProcurementsStats';
import dayjs from 'dayjs';

const LastDate = () => {
    const {data} = useProcuremtns();
    const value = useMemo(() => {
        if (!data?.latest_contract_date) return '-';
        return dayjs(data.latest_contract_date, {format: 'YYYY-MM-DD'}).format('DD.MM.YYYY');
    }, [data?.latest_contract_date]);
    return (
        <StatisticItem 
            name="Последний заключённый контракт"
            value={value}
            icon={<HiClipboardDocumentCheck />}
        />
    )
}

export default LastDate;