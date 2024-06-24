import { Tooltip, Space } from "antd"
import { HiMiniPencilSquare } from "react-icons/hi2";
import styles from './Controls.module.scss';
import { User } from "@/Types";
import {usePrivateStore} from '../../../../Store/Store';


type iControls = {
    item: User.WithCompany;
}

const Controls = (props: iControls) => {
    const openEditModal = usePrivateStore((state) => state.actions.openEditModal);
    return (
        <Space 
            size={8}
            direction="horizontal">
            <Tooltip title="Редактировать">
                <div
                    onClick={() => {
                        openEditModal(props.item)
                    }} 
                    className={styles.control}>
                    <HiMiniPencilSquare />
                </div>
            </Tooltip>
        </Space>
    )
}


export default Controls;