import PageTitle from '@/Components/PageTitle/PageTitle';
import Controls from './Modules/Controls/Controls';
import styles from './Header.module.scss';


const Header = () => {
    return (
        <div className={styles.wrapper}>
            <PageTitle>
                Заявки
            </PageTitle>
            <Controls />
        </div>
    )
}

export default Header;