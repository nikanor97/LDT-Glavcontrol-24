import Block from "../../Components/Block/Block"
import {Form, Col, Row, Input, InputNumber, Button, FormInstance} from 'antd';
import { HiMiniTrash, HiMiniPlus } from "react-icons/hi2";
import Card from './Components/Card/Card';
import styles from './ItemsForm.module.scss';

type iItemsForm = {
    form: FormInstance;
}

const ItemsForm = (props: iItemsForm) => {
    return (
        <Block title="Детали по товарам">
            <Form.List name="products">
                {(fields, {add, remove}) => {
                    return (
                        <>
                            {fields.map((field) => (
                                <Card 
                                    allowDelete={Boolean(fields.length > 1)}
                                    key={field.key}
                                    field={field}
                                    onDelete={remove}
                                    form={props.form}
                                />
                            ))}
                            <div className={styles.addItems}>
                                <Button 
                                    onClick={() => add({})}
                                    icon={<HiMiniPlus />}
                                    type="link">
                                    Добавить товар
                                </Button>
                            </div>
                        </>
                    )
                }}
            </Form.List>
            
        </Block>
    )
}

export default ItemsForm;