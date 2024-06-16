import Link from 'next/link';
import getRoute from '@/Routes/Routes';
import BlockTitle from "../../../../Components/BlockTitle/BlockTitle"
import {usePrivateStore} from '../../../../Store/Store';
import styles from './Header.module.scss';
import {DatePicker} from 'antd';
import dayjs from 'dayjs';
import { useDateByQuarter } from '@/Hooks/Date/useDateByQuarter';



const Header = () => {
    const setOrderDates = usePrivateStore((state) => state.actions.setOrderDates);
    const params = usePrivateStore((state) => state.orders);
    const value = useDateByQuarter(params.quarter, params.year);

    return (
        <div className={styles.wrapper}>
            <Link href={getRoute.lk.orders}>
                <BlockTitle className={styles.title}>
                    Закупки
                </BlockTitle>
            </Link>
            <DatePicker
                picker="quarter"
                value={value}
                size="large"
                onChange={(value) => {
                    setOrderDates(
                        value.year(),
                        value.quarter()
                    )
                }}
            />
        </div>
    )
}


export default Header;