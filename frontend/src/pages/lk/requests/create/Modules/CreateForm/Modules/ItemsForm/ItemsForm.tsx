import Block from "../../Components/Block/Block"
import {Form, Col, Row, Input, InputNumber, Button} from 'antd';
import { HiMiniTrash, HiMiniPlus } from "react-icons/hi2";
import Card from './Components/Card/Card';
import styles from './ItemsForm.module.scss';

const ItemsForm = () => {
    return (
        <Block title="Детали по товарам">
            <Form.List name="items">
                {(fields, {add, remove}) => {
                    return (
                        <>
                            {fields.map((field) => (
                                <Card 
                                    allowDelete={Boolean(fields.length > 1)}
                                    key={field.key}
                                    field={field}
                                    onDelete={remove}
                                    path={['items']}
                                />
                            ))}
                            <div className={styles.addItems}>
                                <Button 
                                    onClick={add}
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