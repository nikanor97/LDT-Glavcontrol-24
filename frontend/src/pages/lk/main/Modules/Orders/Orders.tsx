import {Col, Row} from 'antd';
import Graphic from './Modules/Graphic/Graphic';
import styles from './Orders.module.scss';
import Contracts from "./Modules/Contracts/Contracts";
import LastDate from "./Modules/LastDate/LastDate";
import Header from './Modules/Header/Header';
import {useProcuremtns} from './Hooks/useProcurementsStats';
import StateController from '@/Containers/StateController/StateController';


const Orders = () => {
    const {data, isLoading, isError} = useProcuremtns();
    return (
        <div className={styles.wrapper}>
            <Header />
            <StateController 
                state={{isLoading, isError}}
                data={data}>
                <Row gutter={[16,16]}>
                    <Col span={8}>
                        <Row gutter={[16, 16]}>
                            <Col span={24}>
                                <Contracts />
                            </Col>
                            <Col span={24}>
                                <LastDate />
                            </Col>
                        </Row>
                    </Col>
                    <Col span={16}>
                        <Graphic />
                    </Col>
                </Row>
            </StateController>
        </div>
    )
}


export default Orders;