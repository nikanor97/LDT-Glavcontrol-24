import {useMemo} from 'react';
import styles from './Graphic.module.scss';
import {useProcuremtns} from '../../Hooks/useProcurementsStats';
import {ResponsiveContainer, XAxis, CartesianGrid, Tooltip, Area, AreaChart} from 'recharts';
import {cloneDeep} from 'lodash';
import dayjs from 'dayjs'

const Graphic = () => {
    const {data} = useProcuremtns();
    const clearData = useMemo(() => {
        if (!data?.contracts_stats) return null;
        const result = cloneDeep(data.contracts_stats);
        result.forEach((point) => {
            point.contracts_date = dayjs(point.contracts_date).format('MMM')
        })
        return result;
    }, [data]);
    if (!clearData) return null;
    
    return (
        <div className={styles.wrapper}>
            <div className={styles.title}>
                Количество размещенных контрактов
            </div>
            <div className={styles.graphic}>
                <ResponsiveContainer 
                    width="100%" 
                    height="100%">
                    <AreaChart
                        width={500}
                        height={300}
                        data={clearData}>
                        <defs>
                            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#D92D20" stopOpacity={0.5}/>
                                <stop offset="95%" stopColor="#D92D20" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid 
                            strokeDasharray="1 3"
                            horizontal={false} 
                        />
                        <XAxis 
                            dataKey="contracts_date" 
                        />
                        <Tooltip />
                        <Area 
                            type="monotone" 
                            dataKey="amount_contracts" 
                            stroke="#D92D20" 
                            dot={false}
                            name="Количество котнтрактов"
                            fill="url(#colorUv)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
            
        </div>
    )
}

export default Graphic;