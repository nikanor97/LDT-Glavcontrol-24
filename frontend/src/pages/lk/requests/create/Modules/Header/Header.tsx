import PageTitle from "@/Components/PageTitle/PageTitle";
import styles from './Header.module.scss';
import {Breadcrumb} from 'antd';
import getRoute from '@/Routes/Routes';
import Link from 'next/link';
import { useIsEdit } from "../../Hooks/useIsEdit";


const Header = () => {
    const isEdit = useIsEdit();

    return (
        <div className={styles.wrapper}>
            <Breadcrumb 
                items={[
                    {
                        title: (
                            <Link href={getRoute.lk.requests}>
                                Заявки
                            </Link>
                        ),
                    },
                    {
                        title: isEdit ? 'Редаетирование заявки' : 'Новая заявка',
                    },
                ]}
            />
            <PageTitle className={styles.title}>
                {
                    isEdit ? 'Редактировать заявку' : 'Создать новую заявку'
                }
            </PageTitle>
        </div>
    )
}

export default Header;