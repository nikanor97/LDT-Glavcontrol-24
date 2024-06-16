import {useMemo} from 'react';
import StatisticItem from "../../Components/StatsticItem/StatisticItem";
import { HiBanknotes } from "react-icons/hi2";
import { HiClock } from "react-icons/hi";
import {useProcuremtns} from '../../Hooks/useProcurementsStats';
import { getMeasurementNumber } from "@/Utils/Transform/getMeasurementNumber";


const Contracts = () => {
    const {data} = useProcuremtns();
    const value = data?.amount_contracts || '-'
    
    return (
        <StatisticItem 
            name="Сумма размещённых контрактов"
            value={
                <>
                    {value}
                    {" "}
                    <span style={{
                        fontSize: '17px',
                        lineHeight: '20px'
                    }}>
                        млн
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