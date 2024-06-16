import {Tooltip, Space} from 'antd';
import { HiOutlinePencilAlt, HiOutlineTrash } from "react-icons/hi";
import styles from './Controls.module.scss';
import { Company } from '@/Types';
import {usePrivateStore} from '../../../../Store/Store';


type iControls = {
    item: Company.ExistItem;
}

const Controls = (props: iControls) => {
    const openDrawer = usePrivateStore((state) => state.actions.openDrawer)
    return (
        <Space direction="horizontal">
            <Tooltip title="Редактировать заявку">
                <div    
                    onClick={() => {
                        openDrawer(props.item);
                    }}
                    className={styles.control}>
                    <HiOutlinePencilAlt />
                </div>    
            </Tooltip>
        </Space>
    )
}

export default Controls;