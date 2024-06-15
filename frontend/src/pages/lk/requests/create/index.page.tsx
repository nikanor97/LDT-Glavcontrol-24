import {App} from '@/Types'
import UserLayout from '@/Layouts/UserLayout/UserLayout';
import CreateForm from './Modules/CreateForm/CreateForm';
import Header from './Modules/Header/Header';
import styles from './index.module.scss';

const RequestsCreate:App.Next.NextPage = () => {
    return (
        <div className={styles.wrapper}>
            <Header />
            <CreateForm />
        </div>
    )
}

RequestsCreate.Role = ['user'];
RequestsCreate.getLayout = (children) => {
    return (
        <UserLayout>
            {children}
        </UserLayout>
    )
}


export default RequestsCreate;