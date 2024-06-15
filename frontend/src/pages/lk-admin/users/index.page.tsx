import {App} from '@/Types'
import AdminLayout from '@/Layouts/AdminLayout/AdminLayout';
import {ContextComponent} from './Store/Store';
import Header from './Modules/Header/Header';
import UsersTable from './Modules/UsersTable/UsersTable';
import CreateUserDrawer from './Modules/CreateUserDrawer/CreateUserDrawer';

const CompaniesPage:App.Next.NextPage = () => {
    return (
        <ContextComponent>
            <Header />
            <UsersTable />
            <CreateUserDrawer />
        </ContextComponent>
    )
}

CompaniesPage.Role = ['admin'];
CompaniesPage.getLayout = (children) => {
    return (
        <AdminLayout>
            {children}
        </AdminLayout>
    )
}


export default CompaniesPage;