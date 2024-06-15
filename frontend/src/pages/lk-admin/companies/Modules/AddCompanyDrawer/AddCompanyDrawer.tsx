import {Button, Form} from 'antd';
import DrawerModule from "@/Components/Drawer/Drawer";
import {usePrivateStore} from '../../Store/Store';
import CreateCompanyForm from "./Modules/CreateCompanyForm/CreateCompanyForm";
import {useCreateCompanyState} from '@/Hooks/Company/useCreateCompany';
import styles from './AddCompanyDrawer.module.scss';

const AddCompanyDrawer = () => {
    const visible = usePrivateStore((state) => state.addCompany.visible);
    const close = usePrivateStore((state) => state.actions.closeDrawer);
    const state = useCreateCompanyState();
    const [form] = Form.useForm();

    return (
        <DrawerModule 
            width="unset"
            title="Добавить компанию" 
            onClose={close}
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
                <CreateCompanyForm form={form} />
            </div>
        </DrawerModule>
    )
}

export default AddCompanyDrawer;