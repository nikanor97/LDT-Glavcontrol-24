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
import dayjs from 'dayjs';
import Status from './Components/Status/Status';
import Controls from './Components/Controls/Controls';
import {Requests} from '@/Types';

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
                                    dataIndex: 'author_id',
                                    width: 278,
                                    fixed: 'left'
                                },
                                {
                                    title: 'Дата создания',
                                    dataIndex: 'created_at',
                                    width: 278,
                                    render: (value: string) => {
                                        return dayjs(value).format('DD.MM.YYYY HH:mm')
                                    }
                                },
                                {
                                    title: 'Кол-во товаров',
                                    dataIndex: 'id',
                                    width: 278,

                                },
                                {
                                    title: 'Статус',
                                    dataIndex: 'status',
                                    render: (value: Requests.Status) => (
                                        <Status 
                                            status={value}
                                        />
                                    ),
                                    width: 172,
                                },
                                {
                                    title: 'Действия',
                                    width: 140,
                                    render: (item: Requests.Item) => {
                                        return (
                                            <Controls item={item} />
                                        )
                                    }
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