import {useState} from 'react';
import Table from '@/Components/Table/Table';
import {Pagination, Affix} from 'antd';
import styles from './OrdersTable.module.scss';
import classNames from 'classnames';
import StateController from '@/Containers/StateController/StateController';
import {useProcurements} from '@/Hooks/Procurements/useProcurements';
import {usePrivateStore} from '../../Store/Store';
import { getPageByOffset } from '@/Utils/Pagination/getPageByOffset';
import { getOffsetByPage } from '@/Utils/Pagination/getOffsetByPage';

const OrdersTable = () => {
    const [sticked, setSticked] = useState(false);
    const params = usePrivateStore((state) => state.params);
    const changeParams = usePrivateStore((state) => state.actions.changeParams);
    const {data, isError, isLoading} = useProcurements(params)
    return (
        <StateController 
            state={{isLoading, isError}}
            data={data}>
            {
                data && (
                    <div className={styles.wrapper}>
                        <Table 
                            dataSource={data?.items}
                            pagination={false}
                            sticky
                            scroll={{
                                x: '100%'
                            }}
                            rowKey={(record) => record.id}
                            columns={[
                                {
                                    title: 'ID СПГЗ',
                                    dataIndex: 'id',
                                    width: 180,
                                    fixed: 'left'
                                },
                                {
                                    title: 'Наименование СПГЗ',
                                    dataIndex: 'id',
                                    width: 240,
                                },
                                {
                                    title: 'Дата заключения',
                                    dataIndex: 'id',
                                    width: 208,

                                },
                                {
                                    title: 'Цена ГК, руб.',
                                    dataIndex: 'id',
                                    width: 164,

                                },
                                {
                                    title: 'Способ определения поставщика',
                                    dataIndex: 'id',
                                    width: 320,

                                },
                                {
                                    title: 'Основание заключения контракта',
                                    dataIndex: 'id',
                                    width: 384,

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
        </StateController>
    )
}

export default OrdersTable;