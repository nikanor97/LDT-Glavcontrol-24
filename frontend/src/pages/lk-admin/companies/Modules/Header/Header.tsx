
import PageTitle from '@/Components/PageTitle/PageTitle';
import {Button} from 'antd';
import { HiMiniPlus } from "react-icons/hi2";
import {usePrivateStore} from '../../Store/Store';
import styles from './Header.module.scss';

const Header = () => {
    const openDrawer = usePrivateStore((state) => state.actions.openDrawer);
    return (
        <div className={styles.wrapper}>
            <PageTitle>
                Компании
            </PageTitle>
            <Button 
                icon={<HiMiniPlus />}
                size="large"
                onClick={openDrawer}
                type="primary">
                Добавить
            </Button>
        </div>
    )
}

export default Header;