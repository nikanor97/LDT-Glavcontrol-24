import {useState} from 'react';
import Table from '@/Components/Table/Table';
import styles from './UsersTable.module.scss';
import StateController from '@/Containers/StateController/StateController';
import {useAllUsers} from '@/Hooks/User/useAllUsers';
import {User} from '@/Types';
import { ColumnsType } from 'antd/lib/table';
import Permissions from './Components/Permissions/Permissions';
import { Affix, Avatar, Pagination, Space } from 'antd';
import { getUserAvatar } from '@/Utils/User/getUserAvatar/getUserAvatar';
import classNames from 'classnames';
import { getPageByOffset } from '@/Utils/Pagination/getPageByOffset';
import { getOffsetByPage } from '@/Utils/Pagination/getOffsetByPage';
import {usePrivateStore} from '../../Store/Store';


const OrdersTable = () => {
    const [sticked, setSticked] = useState(false);
    const params = usePrivateStore((state) => state.usersListParams);
    const {data, isError, isLoading} = useAllUsers(params);
    const changeParams = usePrivateStore((state) => state.actions.changeParams)
    const columns:ColumnsType<User.WithCompany> = [
        {
            title: 'ФИО',
            dataIndex: 'name',
            width: 264,
            fixed: 'left',
            render: (value, record) => {
                return (
                    <Space 
                        align="center"
                        size={12}
                        direction="horizontal">
                        <Avatar
                            src={getUserAvatar(record.user_id).src}
                            size={24}
                        />
                        <div>
                            {record.user_name}
                        </div>
                    </Space>
                )
            }
        },
        {
            title: 'Email',
            dataIndex: 'user_email',
            width: 192,
        },
        {
            title: 'Права',
            width: 192,
            render: (value, record) => {
                return (
                    <Permissions item={record} />
                )
            }
        },
        {
            title: 'Компания',
            width: 264,
            dataIndex:'company_name'
        },
        {
            title: 'Имя пользователя в Telegram',
            width: 264,
            render: (record: User.WithCompany) => {
                if (!record.user_telegram_username) return '-';
                return record.user_telegram_username;
            }
        },
    ]
    
    return (
        <StateController 
            state={{isLoading, isError}}
            data={data}>
            {
                data && (
                    <div className={styles.wrapper}>
                        <Table 
                            dataSource={data.items}
                            pagination={false}
                            sticky
                            scroll={{
                                x: '100%'
                            }}
                            rowKey={(record) => record.id}
                            columns={columns}
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