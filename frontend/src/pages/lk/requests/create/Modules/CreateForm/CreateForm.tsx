import {useMemo} from 'react';
import {Form, Space, Button, message} from 'antd';
import MainForm from './Modules/MainForm/MainForm';
import ItemsForm from './Modules/ItemsForm/ItemsForm';
import styles from './CreateForm.module.scss';
import {useRequest} from '../../Hooks/useRequest';
import { Requests } from '@/Types';
import { useIsEdit } from '../../Hooks/useIsEdit';
import {useCreateRequest} from '@/Hooks/Requests/useCreateRequest';
import {useUpdateRequest} from '@/Hooks/Requests/useUpdateRequest';
import { getErrorMessage } from '@/Utils/Api/getErrorMessage';

const CreateForm = () => {
    const {data} = useRequest();
    const [form] = Form.useForm();
    const isEdit = useIsEdit();
    const updateRequest = useUpdateRequest();
    const createRequest = useCreateRequest();
    const mergeddata = useMemo<Partial<Requests.WithProduct>>(() => {
        if (data) {
            if (data.products.length) return data;
            else return {
                ...data,
                products: []
            }
        }
        return {};
    }, [data]);
    return (
        <div className={styles.wrapper}>
            <Form 
                form={form}
                initialValues={mergeddata}
                onFinish={async (values) => {
                    try {
                        if (isEdit) {
                            await updateRequest.mutateAsync({
                                id: mergeddata.id,
                                ...values,
                                status: 'ready'
                            })
                        } else {
                            createRequest.mutateAsync({
                                ...values,
                                status: 'ready'
                            })   
                        }
                        message.success('Заявка успешно сохранена')
                    } catch (ex: any) {
                        message.error(getErrorMessage(ex));
                    }
                }}
                className={styles.form}
                layout="vertical">
                <Space 
                    className={styles.space}
                    size={24}
                    direction="vertical">
                    <MainForm />
                    <ItemsForm form={form} />
                    <div className={styles.controls}>
                        <Button 
                            htmlType="submit"
                            size="large"
                            loading={createRequest.isPending || updateRequest.isPending}
                            type="primary">
                            {isEdit ? 'Опубликовать заявку' : 'Создать заявку'}
                        </Button>
                    </div>
                </Space>
            </Form>
        </div>
    )
}

export default CreateForm;