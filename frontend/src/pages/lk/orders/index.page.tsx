import {App} from '@/Types'
import UserLayout from '@/Layouts/UserLayout/UserLayout';
import Header from './Modules/Header/Header';
import OrdersTable from './Modules/OrdersTable/OrdersTable';
import {ContextComponent} from './Store/Store';

const OrdersPage:App.Next.NextPage = () => {
    return (
        <ContextComponent>
            <Header />
            <OrdersTable />
        </ContextComponent>
    )
}

OrdersPage.Role = ['user'];
OrdersPage.getLayout = (children) => {
    return (
        <UserLayout>
            {children}
        </UserLayout>
    )
}


export default OrdersPage;