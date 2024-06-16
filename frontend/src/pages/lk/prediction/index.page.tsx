import {App} from '@/Types'
import UserLayout from '@/Layouts/UserLayout/UserLayout';
import Header from './Modules/Header/Header';
import PredictionsTable from './Modules/PredictionsTable/PredictionsTable';
import {ContextComponent} from './Store/Store';

const PredictionPage:App.Next.NextPage = () => {
    return (
        <ContextComponent>
            <Header />
            <PredictionsTable />
        </ContextComponent>
    )
}


PredictionPage.Role = ['user'];
PredictionPage.getLayout = (children) => {
    return (
        <UserLayout>
            {children}
        </UserLayout>
    )
}

export default PredictionPage;