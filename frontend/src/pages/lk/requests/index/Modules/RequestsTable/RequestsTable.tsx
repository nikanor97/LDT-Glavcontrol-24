import {useState} from 'react';
import Table from '@/Components/Table/Table';
import {Pagination, Affix, Space, Avatar} from 'antd';
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
import { getUserAvatar } from '@/Utils/User/getUserAvatar/getUserAvatar';



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
                            rowKey={(record) => record.id}
                            scroll={{
                                x: '100%'
                            }}
                            columns={[
                                {
                                    title: 'Автор',
                                    width: 278,
                                    fixed: 'left',
                                    render: (value: Requests.Item) => {
                                        return (
                                            <Space 
                                                size={8}
                                                direction="horizontal">
                                                <Avatar 
                                                    size={20}
                                                    src={getUserAvatar(value.author_id).src}
                                                />
                                                {value.author_name}
                                            </Space>
                                        )
                                    }
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
                                    title: 'Кол-во товаров/услуг',
                                    dataIndex: 'product_count',
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