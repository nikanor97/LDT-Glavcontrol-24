import {useEffect} from 'react';
import Layout from './Layout/Layout';
import {App} from '@/Types';
import styles from './index.module.scss';
import Logo from '@/Img/logo.png';
import Image from 'next/image';
import {Button, Form} from 'antd';
import BasketImg from './Img/basket.png'
import DiscountImg from './Img/discount.png'
import {useRouter} from 'next/router';
import {useUser} from '@/Hooks/User/useUser';
import RegistrationForm from '@/Modules/Auth/RegistrationForm/RegistrationForm';


const LoginPage: App.Next.NextPage = () => {
    const router = useRouter();
    const [form] = Form.useForm();
    const {data: user} = useUser();
    useEffect(() => {
        if (!user) return;
        router.push('/');
    }, [user, router]);

    return (
        <div className={styles.wrapper}>
            <div className={styles.content}>
                <div className={styles.logoWrapper}>
                    <Image 
                        className={styles.logo}
                        src={Logo}
                        quality={100}
                        alt="logo"
                    />
                </div>
                <div className={styles.title}>
                    Регистрация
                </div>
                <div className={styles.formWrapper}>
                    <RegistrationForm 
                        form={form}
                    />
                    <Button     
                        className={styles.btn}
                        size="large"
                        onClick={() => {
                            form.submit();
                        }}
                        type="primary">
                        Зарегистрироваться
                    </Button>
                </div>
            </div>
            <Image 
                src={BasketImg} 
                alt="basket"
                className={styles.basket}
                
            />
            <Image 
                src={DiscountImg}
                alt="discount" 
                className={styles.discount}
            />
        </div>
    )
}

LoginPage.getLayout = (children) => {
    return (
        <Layout>
            {children}
        </Layout>
    )
}

export default LoginPage;