import { required } from "@/Utils/Form/required";
import { Form, Input, DatePicker, FormInstance, message } from "antd";
import {Company} from '@/Types';
import {useCreateCompany} from '@/Hooks/Company/useCreateCompany';
import { getErrorMessage } from "@/Utils/Api/getErrorMessage";
import {useQueryClient} from '@tanstack/react-query';
import {usePrivateStore} from '../../../../Store/Store';
import {queryKey} from '@/Hooks/Company/useCompanies';
import dayjs from "dayjs";

type iCreateCompanyForm = {
    form: FormInstance;
}

const CreateCompanyForm = (props: iCreateCompanyForm) => {
    const createCompany = useCreateCompany();
    const closeDrawer = usePrivateStore((state) => state.actions.closeDrawer);
    const client = useQueryClient();
    return (
        <Form<Company.Item> 
            onFinish={(values) => {
                values.foundation_date = dayjs(values.foundation_date).format('YYYY-MM-DD');

                createCompany.mutate(values, {
                    onSuccess: () => {
                        closeDrawer();
                        message.success('Компания успешно создана');
                        client.resetQueries({
                            queryKey
                        })
                    },
                    onError: (err) => {
                        message.error(getErrorMessage(err))
                    }
                })
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