import React, {useMemo} from 'react';
import ErrorImage from './Images/err.png'
import styles from './Error401.module.scss';
import Link from 'next/link';
import Image from 'next/image';
import routes from '@/Routes/Routes';
import {Button} from 'antd';

type iPage401 = {
    reason: 'role' | 'unauth'
}

const Page401 = (props: iPage401) => {
    const desc = useMemo(() => {
        switch (props.reason) {
            case 'unauth':
                return (
                    <>
                        Для просмотра данной страницы вам необходимо авторизоваться
                        <br />
                        <br />
                        <Link href={routes.login}>
                            <Button 
                                size="large"
                                type="primary">
                                Перейти к авторизации
                            </Button>
                        </Link>
                    </>
                )
            case 'role':
                return (
                    <>
                        Просмотр данной страницы для вашей роли недоступен
                    </>
                )
            default:
                return (
                    <>
                        Запрашиваемые данные не найдены или у вас отсутствует доступ к ним
                    </>
                )
        }
    }, [props.reason]);

    return (
        <div className={styles.content}>
            <div className={styles.img}>
                <Image 
                    src={ErrorImage}
                    alt="401"
                    quality={100}
                />
            </div>          
            <div className={styles.code}>
                401
            </div>
            <div className={styles.title}>
                Отказано в доступе
            </div>
            <div className={styles.desc}>
                {desc}
            </div>
        </div>
    )
}


export default Page401;