import {ResponsiveContainer, BarChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Bar} from 'recharts';
import {useRemains} from '../../Hooks/useRemains';

const Graphic = () => {
    const {data} = useRemains();
    if (!data) return null;
    return (
        <ResponsiveContainer width="100%" height="100%">
            <BarChart data={[
                {
                    name: 'Начало периода',
                    debet: data.saldo_begin_debet,
                    credit: data.saldo_begin_credit
                },
                {
                    name: 'За период',
                    debet: data.saldo_period_debet,
                    credit: data.saldo_period_credit
                },
                {
                    name: 'Конец периода',
                    debet: data.saldo_end_debet,
                    credit: data.saldo_end_credit
                }
            ]}>
                <XAxis dataKey="name" />
                <YAxis 
                    tickFormatter={(value) => {
                        console.log(value);
                        return value;
                    }}
                />
                <Tooltip cursor={false} />
                <Legend />
                <Bar 
                    dataKey="debet" 
                    barSize={48} 
                    fill="#B42318" 
                    name="Дебет"
                />
                <Bar 
                    dataKey="credit" 
                    barSize={48} 
                    fill="#FECDCA" 
                    activeBar={false} 
                    name="Кредит" 
                
                />
            </BarChart>
        </ResponsiveContainer>
    )
}

export default Graphic;