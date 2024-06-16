import {useEffect} from 'react';
import { required } from "@/Utils/Form/required";
import { Form, Input, DatePicker, FormInstance, message } from "antd";
import {Company} from '@/Types';
import {useCreateCompany} from '@/Hooks/Company/useCreateCompany';
import {useUpdateCompany} from '@/Hooks/Company/useUpdateCompany';
import { getErrorMessage } from "@/Utils/Api/getErrorMessage";
import {useQueryClient} from '@tanstack/react-query';
import {usePrivateStore} from '../../../../Store/Store';
import {queryKey} from '@/Hooks/Company/useCompanies';
import { getNormalizedValue, getDateValue } from "@/Utils/Transform/getDateTransform";
import { useIsEdit } from '../../Hooks/useIsEdit';

type iCreateCompanyForm = {
    form: FormInstance;
}

const CreateCompanyForm = (props: iCreateCompanyForm) => {
    const createCompany = useCreateCompany();
    const updateCompany = useUpdateCompany();
    const closeDrawer = usePrivateStore((state) => state.actions.closeDrawer);
    const item = usePrivateStore((state) => state.addCompany.item);
    const client = useQueryClient();
    const isEdit = useIsEdit();

    useEffect(() => {
        if (item) props.form.setFieldsValue(item)
    }, [item]);

    return (
        <Form<Company.Item> 
            onFinish={async (values) => {

                try {
                    if (item) {
                        await updateCompany.mutateAsync({...values, id: item.id})
                        message.success('Компания успешно сохранена');
                    } else {
                        await createCompany.mutateAsync(values)
                        message.success('Компания успешно создана');
                    }
                    closeDrawer();
                    client.resetQueries({
                        queryKey
                    })
                } catch (ex: unknown) {
                    message.error(getErrorMessage(ex))
                }

            }}
            layout="vertical"
            form={props.form}>
            <Form.Item 
                name="name"
                rules={[required('Наименование')]}
                label="Наименование">
                <Input size="large" placeholder="Введите наименование" />
            </Form.Item>
            <Form.Item 
                name="director"
                rules={[required('Директор')]}
                label="Директор">
                <Input size="large" placeholder="ФИО" />
            </Form.Item>
            <Form.Item 
                name="region"
                rules={[required('Регион')]}
                label="Регион">
                <Input size="large" placeholder="Введите регион" />
            </Form.Item>

            <Form.Item
                name="foundation_date"
                rules={[required('Дата основание')]}
                normalize={getNormalizedValue()}
                getValueProps={getDateValue()}
                label="Дата основание">
                <DatePicker  
                    size="large" 
                    placeholder="Выберите дату" 
                    style={{width: '100%'}}
                />
            </Form.Item>
            <Form.Item 
                name="inn"
                rules={[required('ИНН')]}
                label="ИНН">
                <Input size="large" placeholder="Введите ИНН" />
            </Form.Item>
            <Form.Item 
                name="ogrn"
                rules={[required('ОГРН')]}
                label="ОГРН">
                <Input size="large" placeholder="Введите ОГРН" />
            </Form.Item>
        </Form>
    )
}


export default CreateCompanyForm;