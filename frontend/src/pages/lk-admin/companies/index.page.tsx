import {App} from '@/Types'
import AdminLayout from '@/Layouts/AdminLayout/AdminLayout';
import {ContextComponent} from './Store/Store';
import Header from './Modules/Header/Header';
import CompaniesTable from './Modules/CompaniesTable/CompaniesTable';
import AddCompanyDrawer from './Modules/AddCompanyDrawer/AddCompanyDrawer'

const CompaniesPage:App.Next.NextPage = () => {
    return (
        <ContextComponent>
            <Header />
            <CompaniesTable />
            <AddCompanyDrawer />
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