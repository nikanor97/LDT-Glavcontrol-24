import {useMemo} from 'react';
import StatisticItem from "../../Components/StatsticItem/StatisticItem";
import { HiBanknotes } from "react-icons/hi2";
import { HiClock } from "react-icons/hi";
import {useProcuremtns} from '../../Hooks/useProcurementsStats';
import { getMeasurementNumber } from "@/Utils/Transform/getMeasurementNumber";
import {ceil} from 'lodash';

const Contracts = () => {
    const {data} = useProcuremtns();
    // const value = data?.amount_contracts || '-'
    const value = getMeasurementNumber(data?.amount_contracts || 0);
    return (
        <StatisticItem 
            name="Сумма размещённых контрактов"
            value={
                <>
                    {ceil(value.beautified, 2)}
                    {" "}
                    <span style={{
                        fontSize: '17px',
                        lineHeight: '20px'
                    }}>
                        {value.measurement}
                    </span>
                </>
                                    
            }
            extra={
                <span style={{
                    color: '#D92D20'
                }}>
                    <HiClock /> за все время
                </span>
            }
            icon={<HiBanknotes/>}
        />
    )
}

export default Contracts;