import {useState} from 'react';
import Table from '@/Components/Table/Table';
import {Pagination, Affix} from 'antd';
import styles from './RemainsTable.module.scss';
import classNames from 'classnames';
import {usePrivateStore} from '../../Store/Store';
import {useRemains} from '@/Hooks/Remains/useRemains';
import StateController from '@/Containers/StateController/StateController';
import { getPageByOffset } from '@/Utils/Pagination/getPageByOffset';
import { getOffsetByPage } from '@/Utils/Pagination/getOffsetByPage';


const RemainsTable = () => {
    const [sticked, setSticked] = useState(false);
    const params = usePrivateStore((state) => state.params);
    const changeParams = usePrivateStore((state) => state.actions.changeParams);
    const {data, isError, isLoading} = useRemains(params)
    return (
        <StateController 
            data={data}
            state={{isError, isLoading}}>
            {
                data && (
                    <div className={styles.wrapper}>
                        <Table 
                            dataSource={data.items}
                            pagination={false}
                            bordered
                            sticky
                            scroll={{
                                x: '100%'
                            }}
                            columns={[
                                {
                                    title: 'ЦМО',
                                    dataIndex: 'id',
                                    width: 180,
                                    fixed: 'left'
                                },
                                {
                                    title: 'КОЦ',
                                    dataIndex: 'id',
                                    width: 240,
                                },
                                {
                                    title: 'Количество',
                                    dataIndex: 'id',
                                    width: 208,

                                },
                                {
                                    title: 'Показатели',
                                    dataIndex: 'id',
                                    width: 164,

                                },
                                {
                                    title: 'Сальдо на начало периода',
                                    children: [
                                        {
                                            title: 'Дебет',
                                            dataIndex: 'id',
                                            width: 260
                                        }
                                    ]

                                },
                                {
                                    title: 'Сальдо за период',
                                    children: [
                                        {
                                            title: 'Дебет',
                                            dataIndex: 'id',
                                            width: 170
                                        },
                                        {
                                            title: 'Кредит',
                                            dataIndex: 'id',
                                            width: 170
                                        }
                                    ]

                                },
                                {
                                    title: 'Сальдо на конец периода',
                                    children: [
                                        {
                                            title: 'Дебет',
                                            dataIndex: 'id',
                                            width: 260
                                        },
                                    ]

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

export default RemainsTable;