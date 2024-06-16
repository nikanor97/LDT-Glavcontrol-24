import Link from 'next/link';
import getRoute from '@/Routes/Routes';
import BlockTitle from "../../../../Components/BlockTitle/BlockTitle"
import styles from './Header.module.scss';
import {DatePicker} from 'antd';
import {usePrivateStore} from '../../../../Store/Store';
import { useDateByQuarter } from '@/Hooks/Date/useDateByQuarter';


const Header = () => {
    const setRemainsDates = usePrivateStore((state) => state.actions.setRemainsDates);
    const params = usePrivateStore((state) => state.remains);
    const value = useDateByQuarter(params.quarter, params.year);

    return (
        <div className={styles.wrapper}>
            <Link href={getRoute.lk.remains}>
                <BlockTitle className={styles.title}>
                    Остатки
                </BlockTitle>
            </Link>
            <DatePicker
                picker="quarter"
                value={value}
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