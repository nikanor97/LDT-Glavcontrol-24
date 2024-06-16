import {App} from '@/Types'
import UserLayout from '@/Layouts/UserLayout/UserLayout';
import Header from './Modules/Header/Header';
import RequestsTable from './Modules/RequestsTable/RequestsTable';
import {ContextComponent} from './Store/Store';
import DeleteModal from './Modules/DeleteModal/DeleteModal';

const RequestsPage:App.Next.NextPage = () => {
    return (
        <ContextComponent>
            <Header />
            <RequestsTable />
            <DeleteModal />
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