import { Form, Button, message } from "antd"
import {usePrivateStore} from '../../Store/Store';
import RegistrationForm, {useRegistrationState} from '@/Modules/Auth/RegistrationForm/RegistrationForm';
import Drawer from '@/Components/Drawer/Drawer'
import {useQueryClient} from '@tanstack/react-query';
import {getKey} from '@/Hooks/User/useAllUsers';
import styles from './CreateUserDrawer.module.scss';

const CreateUserDrawer = () => {
    const visible = usePrivateStore((state) => state.createUser.visible);
    const close = usePrivateStore((state) => state.actions.closeDrawer);
    const [form] = Form.useForm();
    const state = useRegistrationState();
    const client = useQueryClient();

    return (
        <Drawer
            title="Добавить пользователя" 
            onClose={close}
            width="unset"
            footer={
                <>
                    <Button 
                        loading={
                            state ? state.status === 'pending' : false
                        }
                        size="large"
                        onClick={() => {
                            form.submit();
                        }}
                        type="primary">
                        Добавить
                    </Button>
                </>
            }
            open={visible}>
            <div className={styles.content}>
                <RegistrationForm 
                    form={form} 
                    onSuccess={() => {
                        close();
                        message.success('Пользователь успешно создан');
                        client.refetchQueries({
                            queryKey: getKey
                        })
                    }}
                    onError={(msg) => {
                        message.error(msg)
                    }}
                />
            </div>
        </Drawer>
    )
}

export default CreateUserDrawer;