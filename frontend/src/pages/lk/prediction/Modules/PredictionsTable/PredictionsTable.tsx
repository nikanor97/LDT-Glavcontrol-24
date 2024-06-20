import {useState} from 'react';
import Table from '@/Components/Table/Table';
import {Pagination, Affix} from 'antd';
import styles from './PredictionsTable.module.scss';
import classNames from 'classnames';
import {usePrivateStore} from '../../Store/Store';
import {usePredictions} from '../../Hooks/usePredictions';
import { getOffsetByPage } from '@/Utils/Pagination/getOffsetByPage';
import { getPageByOffset } from '@/Utils/Pagination/getPageByOffset';


const PredictionTable = () => {
    const [sticked, setSticked] = useState(false);
    const {data} = usePredictions();
    const params = usePrivateStore((state) => state.params);
    const changeParams = usePrivateStore((state) => state.actions.changeParams);
    const setSelected = usePrivateStore((state) => state.actions.setSelected);
    const selected = usePrivateStore((state) => state.selected);
    if (!data) return null;
    return (
        <div className={styles.wrapper}>
            <Table
                dataSource={data.items}
                pagination={false}
                sticky
                expandable={{
                    rowExpandable: (record) => Boolean(record.product.description),
                    expandedRowRender: (record) => (
                        <div className={styles.rowDesc}>
                            {record.product.description}
                        </div>
                    )
                }}
                scroll={{
                    x: '100%'
                }}
                rowSelection={{
                    preserveSelectedRowKeys: true,
                    selectedRowKeys: selected,
                    onChange: (selected) => {
                        setSelected(selected.map(String));
                    }
                }}
                rowKey={(record) => {
                    return record.id
                }}
                columns={[
                    {
                        title: 'Наименование',
                        dataIndex: ['product', 'name'],
                        width: 240,
                        fixed: 'left'
                    },
                    {
                        title: 'Цена',
                        dataIndex: ['product', 'price'],
                        width: 240,
                        render: (value: number) => Math.floor(value)
                    },
                    {
                        title: 'Количество',
                        dataIndex: ['product', 'number'],
                        width: 240,

                    },
                    {
                        title: 'Тип',
                        dataIndex: ['product', 'type'],
                        width: 240,
                        render: (value: string | null) => {
                            if (value === null) return '-';
                            return value;
                        }

                    },
                    {
                        title: 'Сумма',
                        dataIndex: ['product', 'amount'],
                        width: 240,
                        render: (value: number) => Math.floor(value)

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
                        total={data.pagination.count}
                        current={getPageByOffset(params.offset, params.limit)}
                        showSizeChanger={false}
                        onChange={(page) => {
                            changeParams({
                                offset: getOffsetByPage(page, params.limit)
                            })
                        }}
                    />
                </div>
            </Affix>
        </div>
    )
}

export default PredictionTable;