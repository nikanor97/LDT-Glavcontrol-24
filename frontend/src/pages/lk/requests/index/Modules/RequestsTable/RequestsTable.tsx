import {useState} from 'react';
import Table from '@/Components/Table/Table';
import {Pagination, Affix} from 'antd';
import styles from './RequestsTable.module.scss';
import classNames from 'classnames';
import {usePrivateStore} from '../../Store/Store';
import {useRequests} from '@/Hooks/Requests/useRequests';
import StateController from '@/Containers/StateController/StateController';
import { getPageByOffset } from '@/Utils/Pagination/getPageByOffset';
import { getOffsetByPage } from '@/Utils/Pagination/getOffsetByPage';

const RequestsTable = () => {
    const [sticked, setSticked] = useState(false);
    const params = usePrivateStore((state) => state.params);
    const changeParams = usePrivateStore((state) => state.actions.changeParams);
    const {data, isError, isLoading} = useRequests(params)
    return (
        <StateController 
            state={{isError, isLoading}}
            data={data}>
            {
                data && (
                    <div className={styles.wrapper}>
                        <Table 
                            dataSource={data.items}
                            pagination={false}
                            sticky
                            rowSelection={{
                                fixed: 'left',
                                type: 'checkbox'
                            }}
                            rowKey={(record) => record.id}
                            scroll={{
                                x: '100%'
                            }}
                            columns={[
                                {
                                    title: 'Автор',
                                    dataIndex: 'id',
                                    width: 278,
                                    fixed: 'left'
                                },
                                {
                                    title: 'Дата создания',
                                    dataIndex: 'id',
                                    width: 278,
                                },
                                {
                                    title: 'Кол-во товаров',
                                    dataIndex: 'id',
                                    width: 278,

                                },
                                {
                                    title: 'Статус',
                                    dataIndex: 'id',
                                    render: () => 'badge',
                                    width: 172,
                                }
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

export default RequestsTable;