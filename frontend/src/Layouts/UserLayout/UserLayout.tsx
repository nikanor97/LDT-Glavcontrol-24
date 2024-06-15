import LkLayout, {Menu, iMenuItem} from '../LkLayout/LkLayout';
import Routes from '@/Routes/Routes';
import { HiHome, HiClipboardDocumentCheck, HiChartBar, HiCalculator, HiClipboardDocument } from "react-icons/hi2";

type iUserLayout = {
    children: React.ReactNode;
}

export const UserLayout = (props: iUserLayout) => {
    return (
        <LkLayout menu={
            <Menu 
                items={[
                    {
                        text: 'Главная',
                        icon: <HiHome />,
                        link: Routes.lk.main,
                        exact: true
                    },
                    {
                        text: 'Закупки',
                        icon: <HiClipboardDocumentCheck />,
                        link: Routes.lk.orders
                    },
                    {
                        text: 'Заявки',
                        icon: <HiClipboardDocument />,
                        link: Routes.lk.requests
                    },
                    {
                        text: 'Прогноз',
                        icon: <HiChartBar />,
                        link: Routes.lk.prediction
                    },
                    {
                        text: 'Остатки',
                        icon: <HiCalculator />,
                        link: Routes.lk.remains
                    },
                ]}
            />
        }>
            {props.children}
        </LkLayout>
    )
}

export default UserLayout;