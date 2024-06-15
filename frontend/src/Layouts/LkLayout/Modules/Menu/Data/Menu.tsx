import {iMenuItem} from '../types';
import { HiHome, HiClipboardDocumentCheck, HiChartBar, HiCalculator, HiClipboardDocument } from "react-icons/hi2";

import Routes from '@/Routes/Routes';

export const data: iMenuItem[] = [
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
]

export default data;