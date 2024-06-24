import { Form, Button, message } from "antd"
import {usePrivateStore} from '../../Store/Store';
import RegistrationForm, {useRegistrationState} from '@/Modules/Auth/RegistrationForm/RegistrationForm';
import Drawer from '@/Components/Drawer/Drawer'
import {useQueryClient} from '@tanstack/react-query';
import {getKey} from '@/Hooks/User/useAllUsers';
import styles from './CreateUserDrawer.module.scss';
import { useRegistration } from "@/Hooks/User/useRegistration";
import { getErrorMessage } from "@/Utils/Api/getErrorMessage";

const CreateUserDrawer = () => {
    const visible = usePrivateStore((state) => state.createUser.visible);
    const close = usePrivateStore((state) => state.actions.closeDrawer);
    const [form] = Form.useForm();
    const state = useRegistrationState();
    const client = useQueryClient();
    const registration = useRegistration();

    return (
        <Drawer
            destroyOnClose
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
                    mode="new"
                    form={form} 
                    onFinish={(values) => {
                        registration.mutate(values, {
                            onSuccess: () => {
                                close();
                                message.success('Пользователь успешно создан');
                                client.refetchQueries({
                                    queryKey: getKey
                                })
                            },
                            onError: (ex) => {
                                message.error(getErrorMessage(ex))
                            }
                        })

                    }}
                />
            </div>
        </Drawer>
    )
}

export default CreateUserDrawer;