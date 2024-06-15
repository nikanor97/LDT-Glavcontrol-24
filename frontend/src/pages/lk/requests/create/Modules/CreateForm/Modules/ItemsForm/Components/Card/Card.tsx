import {Row, Col, Button, Form, Input, InputNumber, FormListFieldData} from 'antd';
import { HiMiniTrash} from "react-icons/hi2";
import styles from './Card.module.scss';
import { NamePath } from 'antd/es/form/interface';
import { isNumber } from 'lodash';

type iCard = {
    field: FormListFieldData;
    onDelete: (index: number | number[]) => any;
    allowDelete: boolean;
    path: NamePath
}

export const Card = (props: iCard) => {
    const {field} = props;
    
    return (
        <div 
            className={styles.card}
            key={field.key}>
            <Row gutter={[16,0]}>
                <Col span={6}>
                    <Form.Item 
                        name={[field.name, 'name']}
                        label="Наименование">
                        <Input placeholder="Введите наименование" size="large" />
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item 
                        name={[field.name, 'price']}
                        label="Цена">
                        <InputNumber placeholder="Введите цену" size="large" />
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item 
                        name={[field.name, 'count']}
                        label="Количество">
                        <InputNumber placeholder="Введите количество" size="large" />
                    </Form.Item>
                </Col>
                <Col span={6}>
                    <Form.Item 
                        shouldUpdate
                        label="Сумма">
                        {(form) => {
                            const price = form.getFieldValue([...props.path,field.name, 'price']);
                            const count = form.getFieldValue([...props.path,field.name, 'count']);
                            let total: string | number = '';
                            if (isNumber(price) && isNumber(count)) {
                                total = price * count;
                            }
                            return (    
                                <Input placeholder="Мы расчитаем сумму" size="large" disabled value={total} />
                            )
                        }}
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