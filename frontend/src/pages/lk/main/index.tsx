import {App} from '@/Types'
import UserLayout from '@/Layouts/UserLayout/UserLayout';
import PageTitle from '@/Components/PageTitle/PageTitle';
import Company from './Modules/Company/Company';
import Orders from './Modules/Orders/Orders';
import Remains from './Modules/Remains/Remains';
import styles from './index.module.scss';
import {ContextComponent as StoreContext} from './Store/Store';

const MainPage:App.Next.NextPage = () => {
    return (
        <StoreContext>
            <div className={styles.wrapper}>
                <PageTitle>
                    Главная
                </PageTitle>
                <Company />
                <Orders />
                <Remains />
            </div>
        </StoreContext>
    )
}

MainPage.Role = ['user'];
MainPage.getLayout = (children) => {
    return (
        <UserLayout>
            {children}
        </UserLayout>
    )
}


export default MainPage;