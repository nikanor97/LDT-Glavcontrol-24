import {useUser} from '@/Hooks/User/useUser';
import Loader from '@/Components/Loader/Loader';
import styles from './GetUser.module.scss';

type iCheckAuth = {
    children: React.ReactNode;
}

//Контейнер для проверки данных авторизации
const GetUser = (props: iCheckAuth) => {
    const {isPending} = useUser();
    if (isPending) {
        return (
            <div className={styles.wrapper}>
                <Loader 
                    text="Загрузка данных пользователя..."
                />
            </div>
        )
    }
    return props.children;
}

export default GetUser;