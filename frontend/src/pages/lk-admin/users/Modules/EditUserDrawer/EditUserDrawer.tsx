import {useEffect} from 'react';
import { Form, Button, message } from "antd"
import {usePrivateStore} from '../../Store/Store';
import RegistrationForm, {useRegistrationState} from '@/Modules/Auth/RegistrationForm/RegistrationForm';
import Drawer from '@/Components/Drawer/Drawer'
import {useQueryClient} from '@tanstack/react-query';
import {getKey} from '@/Hooks/User/useAllUsers';
import styles from './EditUserDrawer.module.scss';
import { User } from '@/Types';
import { useSaveUser } from '@/Hooks/User/useSaveUser';
import { getErrorMessage } from '@/Utils/Api/getErrorMessage';

const CreateUserDrawer = () => {
    const visible = usePrivateStore((state) => state.editUser.visible);
    const item = usePrivateStore((state) => state.editUser.item);
    const close = usePrivateStore((state) => state.actions.closeEditModal);
    const [form] = Form.useForm();
    const state = useRegistrationState();
    const client = useQueryClient();
    const saveUser = useSaveUser();

    useEffect(() => {
        if (item) {
            const user: User.RegUser = {
                id: item.user_id,
                email: item.user_email,
                name: item.user_name,
                permission_create_order: item.user_permission_create_order,
                permission_read_stat: item.user_permission_read_stat,
                role: item.user_role,
                telegram_username: item.user_telegram_username,
                company_id: item.company_id
            }
            form.setFieldsValue(user);
        }
    }, [item])

    return (
        <Drawer
            destroyOnClose
            title="Редактирование пользователя" 
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
                        Сохранить
                    </Button>
                </>
            }
            open={visible}>
            <div className={styles.content}>
                <RegistrationForm 
                    mode="edit"
                    form={form}
                    onFinish={(values) => {
                        if (!item) return;
                        saveUser.mutate({
                            ...values,
                            user_id: item.user_id,
                        }, {
                            onSuccess: () => {
                                close();
                                message.success('Пользователь успешно сохранен');
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