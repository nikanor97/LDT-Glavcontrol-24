import {App} from '@/Types'
import UserLayout from '@/Layouts/UserLayout/UserLayout';
import Header from './Modules/Header/Header';
import RemainsTable from './Modules/RemainsTable/RemainsTable';
import {ContextComponent} from './Store/Store';

const RemainsPage:App.Next.NextPage = () => {
    return (
        <ContextComponent>
            <Header />
            <RemainsTable />
        </ContextComponent>
    )
}

RemainsPage.getLayout = (children) => {
    return (
        <UserLayout>
            {children}
        </UserLayout>
    )
}
RemainsPage.Role = ['user'];

export default RemainsPage;