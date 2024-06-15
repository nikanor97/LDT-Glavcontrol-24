import {useState} from 'react';
import Table from '@/Components/Table/Table';
import styles from './UsersTable.module.scss';
import StateController from '@/Containers/StateController/StateController';
import {useAllUsers} from '@/Hooks/User/useAllUsers';
import {User} from '@/Types';
import { ColumnsType } from 'antd/lib/table';
import Permissions from './Components/Permissions/Permissions';
import { Avatar, Space } from 'antd';
import { getUserAvatar } from '@/Utils/User/getUserAvatar/getUserAvatar';

const OrdersTable = () => {
    const {data, isError, isLoading} = useAllUsers();
    const columns:ColumnsType<User.Item> = [
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
                            src={getUserAvatar(record.id).src}
                            size={24}
                        />
                        <div>
                            {record.name}
                        </div>
                    </Space>
                )
            }
        },
        {
            title: 'Email',
            dataIndex: 'email',
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
                            dataSource={data}
                            pagination={false}
                            sticky
                            scroll={{
                                x: '100%'
                            }}
                            rowKey={(record) => record.id}
                            columns={columns}
                        />
                        
                    </div>
                )
            }
        </StateController>
    )
}

export default OrdersTable;