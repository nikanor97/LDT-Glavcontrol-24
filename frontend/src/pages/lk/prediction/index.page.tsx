import {App} from '@/Types'
import UserLayout from '@/Layouts/UserLayout/UserLayout';
import Header from './Modules/Header/Header';
import PredictionsTable from './Modules/PredictionsTable/PredictionsTable';

const PredictionPage:App.Next.NextPage = () => {
    return (
        <div>
            <Header />
            <PredictionsTable />
        </div>
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