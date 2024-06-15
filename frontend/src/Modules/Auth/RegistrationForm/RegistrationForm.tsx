import {Form, FormInstance, Input, Switch, Space} from 'antd';
import * as Api from '@/Api'
import {iApi} from '@/Api/Auth/types';
import {useRegistration} from '@/Hooks/User/useRegistration';
import styles from './RegistrationForm.module.scss';
import { required } from '@/Utils/Form/required';
import { getErrorMessage } from '@/Utils/Api/getErrorMessage';
export {useRegistrationState} from '@/Hooks/User/useRegistration';

type iRegistrationForm = {
    form: FormInstance;
    onSuccess?: () => any;
    onError?: (text: string) => any;
}

const RegistrationForm = (props: iRegistrationForm) => {
    const registration = useRegistration();
    return (
        <Form<iApi.iRegistration>
            onFinish={(values) => {
                registration.mutate(values, {
                    onSuccess: () => {
                        props.onSuccess && props.onSuccess();
                    },
                    onError: (err) => {
                        props.onError && props.onError(getErrorMessage(err));
                    }
                })
            }}
            form={props.form}
            initialValues={{
                permission_read_stat: false,
                permission_create_order: false
            }}
            layout="vertical">
            <div className={styles.block}>
                <div className={styles.title}>
                    Основная информация
                </div>
                <Form.Item rules={[required('ФИО')]} name="name" label="ФИО">
                    <Input size="large" placeholder="Введите ФИО" />
                </Form.Item>
                <Form.Item rules={[required('Email')]} name="email" label="Email">
                    <Input size="large" placeholder="Введите email" />
                </Form.Item>
                <Form.Item rules={[required('Пароль')]} name="password" label="Пароль">
                    <Input.Password  size="large" placeholder="Пароль" />
                </Form.Item>
            </div>
            <div className={styles.block}>
                <div className={styles.title}>
                    Права
                </div>
                <Space 
                    className={styles.space}
                    size={16}
                    direction="vertical">
                    <div className={styles.switch}>
                        Просмотр статистики
                        <Form.Item noStyle name="permission_read_stat">
                            <Switch />
                        </Form.Item>
                    </div>
                    <div className={styles.switch}>
                        Создание заявок
                        <Form.Item noStyle name="permission_create_order">
                            <Switch />
                        </Form.Item>
                    </div>
                </Space>

            </div>
        </Form>
    )
}

export default RegistrationForm;