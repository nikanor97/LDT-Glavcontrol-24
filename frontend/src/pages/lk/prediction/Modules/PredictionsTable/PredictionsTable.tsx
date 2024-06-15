import {useState} from 'react';
import Table from '@/Components/Table/Table';
import {Pagination, Affix} from 'antd';
import styles from './PredictionsTable.module.scss';
import classNames from 'classnames';

const PredictionTable = () => {
    const [sticked, setSticked] = useState(false);
    return (
        <div className={styles.wrapper}>
            <Table 
                dataSource={new Array(99).fill('').map((item, index) => ({id: index}))}
                pagination={false}
                sticky
                scroll={{
                    x: '100%'
                }}
                rowKey={(record) => record.id}
                expandable={{
                    expandedRowRender: () => {
                        return (
                            <div>
                                expand content
                            </div>
                        )
                    }
                }}
                columns={[
                    {
                        title: 'Наименование',
                        dataIndex: 'id',
                        width: 240,
                        fixed: 'left'
                    },
                    {
                        title: 'Цена',
                        dataIndex: 'id',
                        width: 240,
                    },
                    {
                        title: 'Количество',
                        dataIndex: 'id',
                        width: 240,

                    },
                    {
                        title: 'Сумма',
                        dataIndex: 'id',
                        width: 240,

                    },
                ]}
            />
            <Affix 
                onChange={(value) => {
                    if (value) setSticked(true)
                    else setSticked(false);
                }}
                offsetBottom={0}>
                <div className={classNames(styles.pagination, {
                    [styles.paginationActive]: sticked
                })}>
                    <Pagination 
                        hideOnSinglePage
                        total={200}
                        current={1}
                        showSizeChanger={false}
                    />
                </div>
            </Affix>
        </div>
    )
}

export default PredictionTable;