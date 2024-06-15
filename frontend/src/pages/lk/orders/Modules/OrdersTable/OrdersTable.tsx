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
import dayjs from 'dayjs';

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
                                    dataIndex: 'spgz_id',
                                    width: 180,
                                },
                                {
                                    title: 'Наименование СПГЗ',
                                    dataIndex: 'spgz_name',
                                    width: 240,
                                    fixed: 'left'
                                },
                                {
                                    title: 'Дата заключения',
                                    dataIndex: 'procurement_date',
                                    width: 208,
                                    render: (value) => {
                                        return dayjs(value, {format: 'YYYY-MM-DD'}).format('DD.MM.YYYY')
                                    }

                                },
                                {
                                    title: 'Цена ГК, руб.',
                                    dataIndex: 'price',
                                    width: 164,
                                    render: (value) => {
                                        if (typeof value !== 'number') return '-'
                                        return Math.floor(value);
                                    }

                                },
                                {
                                    title: 'Способ определения поставщика',
                                    dataIndex: 'way_to_define_supplier',
                                    width: 320,

                                },
                                {
                                    title: 'Основание заключения контракта',
                                    dataIndex: 'contract_basis',
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