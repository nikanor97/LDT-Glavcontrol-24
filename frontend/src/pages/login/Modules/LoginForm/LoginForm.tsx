import {useEffect} from 'react';
import {Form, Input, Button, message} from 'antd';
import styles from './LoginForm.module.scss';
import { required } from '@/Utils/Form/required';
import {iApi} from '@/Api/Auth/types';
import {useLogin} from '../../Hooks/useLogin';
import { getErrorMessage } from '@/Utils/Api/getErrorMessage';
import {useQueryClient} from '@tanstack/react-query';
import {queryKey as userQueryKey} from '@/Hooks/User/useUser';


type iForm = iApi.iLogin;

const LoginForm = () => {
    const client = useQueryClient();
    const login = useLogin();
    
    return (
        <Form<iForm> 
            onFinish={(values) => {
                login.mutate(values, {
                    onError: (err) => {
                        message.error(getErrorMessage(err));
                    },
                    onSuccess: () => {
                        client.refetchQueries({queryKey:userQueryKey});
                    }
                });
            }}
            layout="vertical">
            <Form.Item 
                rules={[required('логин')]}
                label="Логин"
                name="username">
                <Input 
                    placeholder='Введите логин' 
                    size="large"
                />
            </Form.Item>
            <Form.Item 
                rules={[required('пароль')]}
                label="Пароль"
                name="password">
                <Input.Password 
                    placeholder='Введите пароль' 
                    size="large"
                />
            </Form.Item>
            <Button 
                loading={login.isPending}
                htmlType="submit"
                className={styles.submit}
                size="large"
                type="primary">
                Войти
            </Button>
        </Form>
    )
}

export default LoginForm;