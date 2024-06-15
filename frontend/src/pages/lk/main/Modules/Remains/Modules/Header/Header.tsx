import Link from 'next/link';
import getRoute from '@/Routes/Routes';
import BlockTitle from "../../../../Components/BlockTitle/BlockTitle"
import styles from './Header.module.scss';
import {DatePicker} from 'antd';
import dayjs from 'dayjs';
import {usePrivateStore} from '../../../../Store/Store';


const Header = () => {
    const setRemainsDates = usePrivateStore((state) => state.actions.setRemainsDates);
    return (
        <div className={styles.wrapper}>
            <Link href={getRoute.lk.remains}>
                <BlockTitle className={styles.title}>
                    Остатки
                </BlockTitle>
            </Link>
            <DatePicker
                picker="quarter"
                defaultValue={dayjs()} 
                size="large"
                onChange={(value) => {
                    setRemainsDates(
                        value.year(),
                        value.quarter()
                    )
                }}
            />
        </div>
    )
}

export default Header;