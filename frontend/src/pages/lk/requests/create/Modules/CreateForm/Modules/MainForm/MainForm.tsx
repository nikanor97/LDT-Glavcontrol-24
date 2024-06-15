import Block from "../../Components/Block/Block"
import {Col, Row, Form, Input, DatePicker, InputNumber} from 'antd';

const MainForm = () => {
    return (
        <Block title="Основные данные">
            <Row gutter={[0,16]}>
                {/* 1 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={8}>
                            <Form.Item label="Идетнификатор расчета">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={8}>
                            <Form.Item label="Идентификатор лота ">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={8}>
                            <Form.Item label="Идентификатор заказчика ">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 2 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={7}>
                            <Form.Item label="Дата окончания поставки">
                                <DatePicker placeholder="Выберите дату" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={7}>
                            <Form.Item label="Дата начала поставки">
                                <DatePicker placeholder="Выберите дату" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={10}>
                            <Form.Item label="Объем поставки">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 3 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item label="Адрес поставки">
                                <Input placeholder="Введите адрес" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item label="Адрес в текстовой форме">
                                <Input placeholder="Введите адрес" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 4 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item label="Условия поставки">
                                <Input placeholder="Введите условия" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item label="Год">
                                <DatePicker.YearPicker placeholder="Выберите год" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 5 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item label="Идентификатор ГАР">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item label="Сквозной идентификатор СПГЗ">
                                <Input placeholder="Введите идентификатор" size="large" />
                            </Form.Item>
                        </Col>
                    </Row>
                </Col>
                {/* 6 */}
                <Col span={24}>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item label="Сумма спецификации">
                                <InputNumber placeholder="Введите сумму" size="large" />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item label="Ед. измерения по ОКЕИ">
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