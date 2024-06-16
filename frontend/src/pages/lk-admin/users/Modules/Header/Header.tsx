
import PageTitle from '@/Components/PageTitle/PageTitle';
import {Button} from 'antd';
import { HiOutlineUserAdd } from "react-icons/hi";
import {usePrivateStore} from '../../Store/Store';
import styles from './Header.module.scss';

const Header = () => {
    const openDrawer = usePrivateStore((state) => state.actions.openDrawer)
    return (
        <div className={styles.wrapper}>
            <PageTitle>
                Пользователи
            </PageTitle>
            <Button 
                onClick={openDrawer}
                icon={<HiOutlineUserAdd />}
                size="large"
                type="primary">
                Добавить
            </Button>
        </div>
    )
}

export default Header;