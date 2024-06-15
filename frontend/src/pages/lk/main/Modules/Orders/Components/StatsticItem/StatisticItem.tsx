import React from 'react';
import styles from './StatisticItem.module.scss';
import {Col, Row} from 'antd';


type iStatisticItem = {
    icon: React.ReactNode;
    name: React.ReactNode;
    value: React.ReactNode;
    extra?: React.ReactNode;
}

const StatisticItem = (props: iStatisticItem) => {
    return (
        <div className={styles.wrapper}>
            <Row 
                wrap={false} 
                className={styles.row}>
                <Col>
                    {
                        <div className={styles.icon}>
                            {props.icon}
                        </div>
                    }
                </Col>
                <Col>
                    <div className={styles.value}>
                        {props.value}
                    </div>
                    <div className={styles.name}>
                        {props.name}
                    </div>
                    {
                        props.extra && (
                            <div className={styles.extra}>
                                {props.extra}
                            </div>
                        )
                    }
                </Col>
            </Row>
        </div>
    )
}

export default StatisticItem;