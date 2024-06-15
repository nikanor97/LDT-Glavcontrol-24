import {Form, Space, Button} from 'antd';
import MainForm from './Modules/MainForm/MainForm';
import ItemsForm from './Modules/ItemsForm/ItemsForm';
import styles from './CreateForm.module.scss';

const CreateForm = () => {
    return (
        <div className={styles.wrapper}>
            <Form 
                initialValues={{
                    items: [null]
                }}
                onFinish={(values) => {
                    console.log(values);
                }}
                className={styles.form}
                layout="vertical">
                <Space 
                    className={styles.space}
                    size={24}
                    direction="vertical">
                    <MainForm />
                    <ItemsForm />
                    <div className={styles.controls}>
                        <Button 
                            htmlType="submit"
                            size="large"
                            type="primary">
                            Создать заявку
                        </Button>
                    </div>
                </Space>
            </Form>
        </div>
    )
}

export default CreateForm;