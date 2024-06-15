import {App} from '@/Types'
import UserLayout from '@/Layouts/UserLayout/UserLayout';
import Header from './Modules/Header/Header';
import RequestsTable from './Modules/RequestsTable/RequestsTable';
import {ContextComponent} from './Store/Store';

const RequestsPage:App.Next.NextPage = () => {
    return (
        <ContextComponent>
            <Header />
            <RequestsTable />
        </ContextComponent>
    )
}

RequestsPage.Role = ['user'];
RequestsPage.getLayout = (children) => {
    return (
        <UserLayout>
            {children}
        </UserLayout>
    )
}


export default RequestsPage;