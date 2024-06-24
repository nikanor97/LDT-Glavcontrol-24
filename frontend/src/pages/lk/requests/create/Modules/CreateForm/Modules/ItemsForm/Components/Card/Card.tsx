import {useEffect} from 'react';
import {Row, Col, Button, Form, Input, InputNumber, FormListFieldData, FormInstance, Select} from 'antd';
import { HiMiniTrash} from "react-icons/hi2";
import styles from './Card.module.scss';
import { NamePath } from 'antd/es/form/interface';
import { isNumber } from 'lodash';
import { required } from '@/Utils/Form/required';


type iCard = {
    field: FormListFieldData;
    onDelete: (index: number | number[]) => any;
    allowDelete: boolean;
    form: FormInstance;
}

export const Card = (props: iCard) => {
    const {field} = props;
    const price = Form.useWatch(['products', field.name, 'price'])
    const count = Form.useWatch(['products', field.name, 'number'])

    useEffect(() => {
        let total: string | number = '';
        if (isNumber(price) && isNumber(count)) {
            total = price * count;
        }
        props.form.setFieldValue(['products',field.name, 'amount'], total)
    }, [price, count])

    return (
        <div 
            className={styles.card}
            key={field.key}>
            <Row gutter={[16,0]}>
                <Col className={styles.col}>
                    <Form.Item 
                        rules={[required()]}
                        name={[field.name, 'name']}
                        label="Наименование">
                        <Input placeholder="Введите наименование" size="large" />
                    </Form.Item>
                </Col>
                <Col className={styles.col}>
                    <Form.Item 
                        rules={[required()]}
                        name={[field.name, 'price']}
                        label="Цена">
                        <InputNumber placeholder="Введите цену" size="large" />
                    </Form.Item>
                </Col>
                <Col className={styles.col}>
                    <Form.Item 
                        rules={[required()]}
                        name={[field.name, 'number']}
                        label="Количество">
                        <InputNumber placeholder="Введите количество" size="large" />
                    </Form.Item>
                </Col>
                <Col className={styles.col}>
                    <Form.Item 
                        name={[field.name, 'type']}
                        label="Тип">
                        <Select 
                            placeholder="Выберите тип"
                            size="large">
                            <Select.Option value="Товар">
                                Товар
                            </Select.Option>
                            <Select.Option value="Услуга">
                                Услуга
                            </Select.Option>
                        </Select>
                    </Form.Item>
                </Col>
                <Col className={styles.col}>
                    <Form.Item label="Сумма" name={[field.name, 'amount']}>
                        <Input placeholder="Мы расчитаем сумму" size="large" disabled />
                    </Form.Item>
                </Col>
            </Row>
            <div className={styles.delete}>
                <Button 
                    icon={<HiMiniTrash />}
                    danger
                    disabled={!props.allowDelete}
                    onClick={() => {
                        props.onDelete(field.name);
                    }}
                    type="link">
                    Удалить
                </Button>
            </div>
        </div>
    )
}

export default Card;