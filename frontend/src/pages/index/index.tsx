import {useEffect} from 'react';
import Loader from "@/Components/Loader/Loader";
import {useUserRole} from '@/Hooks/User/useUserRole';
import {useRouter} from 'next/router';
import getRoute from '@/Routes/Routes';
import styles from './index.module.scss';


const RoutingPage = () => {
    const roles = useUserRole();
    const router = useRouter();
    useEffect(() => {
        if (roles.unauth) router.push(getRoute.login)
        else {
            if (roles.user) router.push(getRoute.lk.main);
            else router.push(getRoute.lkAdmin.main);
        }
    }, []);

    return (
        <div className={styles.wrapper}>
            <Loader text="Выполняем маршрутизацию..." />
        </div>
    )
}

export default RoutingPage;