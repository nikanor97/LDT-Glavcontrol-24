import PageTitle from "@/Components/PageTitle/PageTitle";
import styles from './Header.module.scss';
import {Breadcrumb} from 'antd';
import getRoute from '@/Routes/Routes';
import Link from 'next/link';

const Header = () => {
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
                        title: 'Новая заявка',
                    },
                ]}
            />
            <PageTitle className={styles.title}>
                Создать новую заявку
            </PageTitle>
        </div>
    )
}

export default Header;