import {Form, FormInstance, Input, Switch, Space} from 'antd';
import {iApi} from '@/Api/Auth/types';
import styles from './RegistrationForm.module.scss';
import { required } from '@/Utils/Form/required';
import CompanySelect from './Modules/CompanySelect/CompanySelect';
export {useRegistrationState} from '@/Hooks/User/useRegistration';


type iRegistrationForm = {
    form: FormInstance;
    mode: 'new' | 'edit'
    onFinish?: (values: iApi.iRegistration) => any;
}

const RegistrationForm = (props: iRegistrationForm) => {
    return (
        <Form<iApi.iRegistration>
            onFinish={(values) => {
                props.onFinish && props.onFinish(values);
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
                {
                    props.mode === 'new' && (
                        <Form.Item rules={[required('Пароль')]} name="password" label="Пароль">
                            <Input.Password  size="large" placeholder="Пароль" />
                        </Form.Item>
                    )
                }
                <Form.Item rules={[required('Компания')]} name="company_id" label="Компания">
                    <CompanySelect 
                        allowClear 
                        showSearch 
                        size="large" 
                        placeholder="Выберите компанию" 
                        filterOption={(input, option) => 
                            (option?.label || '')
                                .toString()
                                .toLowerCase()
                                .includes(
                                    input.toLowerCase()
                                )}    
                    />
                </Form.Item>
                <Form.Item 
                    rules={[required('Имя в telegram')]}
                    name="telegram_username" 
                    label="Имя пользователя Telegram">
                    <Input size="large" placeholder="Введите имя в telegram" />
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