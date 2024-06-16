import {App} from '@/Types'
import UserLayout from '@/Layouts/UserLayout/UserLayout';
import CreateForm from './Modules/CreateForm/CreateForm';
import Header from './Modules/Header/Header';
import styles from './index.module.scss';
import StateController from '@/Containers/StateController/StateController';
import {useRequest} from './Hooks/useRequest';



const RequestsCreate:App.Next.NextPage = () => {
    const {data, isLoading, isError} = useRequest();
    return (
        <StateController
            loaderFullHeight
            state={{isError, isLoading}}
            data={data}>
            <div className={styles.wrapper}>
                <Header />
                <CreateForm />
            </div>
        </StateController>
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