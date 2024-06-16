import dayjs from "dayjs";
import Block from "../../Components/Block/Block"
import {Col, Row, Form, Input, DatePicker, InputNumber} from 'antd';
import { getDateValue, getNormalizedValue } from "@/Utils/Transform/getDateTransform";

const MainForm = () => {
    return (
        <Block title="Основные данные">
            <Row gutter={[0,16]}>
                {/* 1 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={8}>
                            <Form.Item name="calculation_id" label="Идетнификатор расчета">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={8}>
                            <Form.Item name="lot_id" label="Идентификатор лота ">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={8}>
                            <Form.Item name="client_id" label="Идентификатор заказчика ">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 2 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={7}>
                            <Form.Item 
                            
                                normalize={getNormalizedValue()}
                                getValueProps={getDateValue()} 
                                name="shipment_end_date" 
                                label="Дата окончания поставки">
                                <DatePicker placeholder="Выберите дату" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={7}>
                            <Form.Item 
                            
                                normalize={getNormalizedValue()}
                                getValueProps={getDateValue()} 
                                name="shipment_start_date" 
                                label="Дата начала поставки">
                                <DatePicker placeholder="Выберите дату" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={10}>
                            <Form.Item 
                            
                                name="shipment_volume"
                                label="Объем поставки">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 3 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={24}>
                            <Form.Item 
                            
                                name="shipment_address"
                                label="Адрес поставки">
                                <Input placeholder="Введите адрес" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 4 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item name="shipment_terms" label="Условия поставки">
                                <Input placeholder="Введите условия" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item 
                            
                                normalize={getNormalizedValue('YYYY')}
                                getValueProps={(value) => {
                                    return {
                                        value: value && dayjs(`01.01.${value}`, {format: 'DD.MM.YYYY'})
                                    };
                                }}
                                name="year" 
                                label="Год">
                                <DatePicker.YearPicker placeholder="Выберите год" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 5 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item name="gar_id" label="Идентификатор ГАР">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item name="spgz_end_id" label="Сквозной идентификатор СПГЗ">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 6 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item name="amount" label="Сумма спецификации">
                                <InputNumber placeholder="Введите сумму" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item name="unit_of_measurement" label="Ед. измерения по ОКЕИ">
                                <Input placeholder="Введите единицы измерения" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </Block>
    )
}

export default MainForm;