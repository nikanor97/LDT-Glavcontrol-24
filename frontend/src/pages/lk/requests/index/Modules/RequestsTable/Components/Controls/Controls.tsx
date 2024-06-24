import {Space, Tooltip, Modal} from 'antd';
import { HiOutlinePencilAlt, HiOutlineTrash, HiDownload } from "react-icons/hi";

import { HiArrowDownTray} from "react-icons/hi2";
import {Requests} from '@/Types';
import {usePrivateStore} from '../../../../Store/Store';
import styles from './Controls.module.scss';
import getRoute from '@/Routes/Routes';
import Link from 'next/link'

type iControls = {
    item: Requests.Item;
}


const Controls = (props: iControls) => {
    const {item} = props;
    const openDeleteModal = usePrivateStore((state) => state.actions.openDeleteModal);
    return (
        <Space direction="horizontal">
            {
                item.status !== 'draft' && (

                    <Tooltip title="Скачать JSON">
                        <div className={styles.control}>
                            <HiArrowDownTray />
                        </div>
                    </Tooltip>
                )
            }
            <Tooltip title="Редактировать заявку">
                <Link href={getRoute.lk.createRequest(item.id)}>
                    <div className={styles.control}>
                        <HiOutlinePencilAlt />
                    </div>
                </Link>
            </Tooltip>
            <Tooltip title="Скачать документацию">
                <Link 
                    target="_blank" 
                    href={getRoute.lk.uploadRequestDocumentation(item.id)}>
                    <div className={styles.control}>
                        <HiDownload />
                    </div>
                </Link>
            </Tooltip>
            {/* <Tooltip title="Удалить заявку">
                <div 
                    onClick={() => {
                        openDeleteModal(item);
                    }}
                    className={styles.control}>
                    <HiOutlineTrash />
                </div>
            </Tooltip> */}
        </Space>
    )
}

export default Controls;