import {useState} from 'react';
import Table from '@/Components/Table/Table';
import {Pagination, Affix} from 'antd';
import styles from './CompaniesTable.module.scss';
import classNames from 'classnames';
import StateController from '@/Containers/StateController/StateController';
import {useCompanies} from '@/Hooks/Company/useCompanies';
import {usePrivateStore} from '../../Store/Store';
import { getPageByOffset } from '@/Utils/Pagination/getPageByOffset';
import { getOffsetByPage } from '@/Utils/Pagination/getOffsetByPage';
import Controls from './Components/Controls/Controls';
import dayjs from 'dayjs';
import { Company } from '@/Types';

const OrdersTable = () => {
    const [sticked, setSticked] = useState(false);
    const params = usePrivateStore((state) => state.params);
    const changeParams = usePrivateStore((state) => state.actions.changeParams);
    const {data, isError, isLoading} = useCompanies(params)
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
                                    title: 'Наименование',
                                    dataIndex: 'name',
                                    width: 146,
                                    fixed: 'left'
                                },
                                {
                                    title: 'Директор',
                                    dataIndex: 'director',
                                    width: 146,
                                },
                                {
                                    title: 'Регион',
                                    dataIndex: 'region',
                                    width: 146,

                                },
                                {
                                    title: 'Дата основания',
                                    dataIndex: 'foundation_date',
                                    width: 192,
                                    render: (value) => {
                                        return dayjs(value, {format:'YYYY-MM-DD'}).format('DD.MM.YYYY')
                                    }

                                },
                                {
                                    title: 'ИНН',
                                    dataIndex: 'inn',
                                    width: 140,

                                },
                                {
                                    title: 'ОГРН',
                                    dataIndex: 'ogrn',
                                    width: 140,
                                },
                                {
                                    title: 'Действия',
                                    width: 140,
                                    render: (item: Company.ExistItem) => {
                                        return (
                                            <Controls item={item} />
                                        )
                                    }

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