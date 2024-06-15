import Link from 'next/link';
import getRoute from '@/Routes/Routes';
import BlockTitle from "../../../../Components/BlockTitle/BlockTitle"
import {usePrivateStore} from '../../../../Store/Store';
import styles from './Header.module.scss';
import {DatePicker} from 'antd';
import dayjs from 'dayjs';

const Header = () => {
    const setOrderDates = usePrivateStore((state) => state.actions.setOrderDates);
    return (
        <div className={styles.wrapper}>
            <Link href={getRoute.lk.orders}>
                <BlockTitle className={styles.title}>
                    Закупки
                </BlockTitle>
            </Link>
            <DatePicker
                picker="quarter"
                defaultValue={dayjs()} 
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