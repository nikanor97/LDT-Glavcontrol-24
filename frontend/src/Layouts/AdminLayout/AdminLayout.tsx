import LkLayout, {Menu} from '../LkLayout/LkLayout';
import Routes from '@/Routes/Routes';
import { HiBuildingOffice2, HiUsers } from "react-icons/hi2";


type iUserLayout = {
    children: React.ReactNode;
}

export const UserLayout = (props: iUserLayout) => {
    return (
        <LkLayout menu={
            <Menu 
                items={[
                    {
                        text: 'Компании',
                        icon: <HiBuildingOffice2 />,
                        link: Routes.lkAdmin.main,
                        exact: true
                    },
                    {
                        text: 'Пользователи',
                        icon: <HiUsers />,
                        link: Routes.lkAdmin.users
                    },
                ]}
            />
        }>
            {props.children}
        </LkLayout>
    )
}

export default UserLayout;