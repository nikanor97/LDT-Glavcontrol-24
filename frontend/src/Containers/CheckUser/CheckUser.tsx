import {App} from '@/Types';
import LayoutContainer from '@/Containers/Layout/Layout';
import { useRoleValid } from './Hooks/useRoleValid';
import { useUserRole } from '@/Hooks/User/useUserRole';
import Error401 from '@/Modules/Error401/Error401';
import styles from './CheckUser.module.scss';

type iCheckUser = Pick<App.Next.NextPage, 'getLayout' | 'Role'> & {
    children: React.ReactElement;
}
//Контейнер для проверки роли пользователя и доступов объявленных на странице
const CheckUser = (props: iCheckUser) => {
    const isValid = useRoleValid(props.Role);
    const userRole = useUserRole();
    //Возвращаем лейаут если все хорошо с настройками страницы
    if (isValid) {
        return (
            <LayoutContainer getLayout={props.getLayout}>
                {props.children}
            </LayoutContainer>
        );
    } else {
        //Для кейсов с ошибкой используем лейаут по умолчанию
        if (userRole.unauth) {
            return (
                <LayoutContainer>
                    <div className={styles.authPage}>
                        <Error401 reason="unauth" />
                    </div>
                </LayoutContainer>
            )
        } else {
            return (
                <LayoutContainer>
                    <div className={styles.authPage}>
                        <Error401 reason="role" />
                    </div>
                </LayoutContainer>
            )
        }
    }
}

export default CheckUser;