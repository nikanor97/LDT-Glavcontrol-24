import { Space, Avatar, Dropdown } from "antd";
import styles from './User.module.scss';
import {useUser} from '@/Hooks/User/useUser';
import { getUserAvatar } from "@/Utils/User/getUserAvatar/getUserAvatar";
import UserMenu from '../UserMenu/UserMenu';

const User = () => {
    const {data} = useUser();
    if (!data) return data;
    return (
        <Dropdown 
            dropdownRender={() => <UserMenu />}>
            <Space 
                size={16}
                direction="horizontal">
                <div className={styles.name}>
                    {data.name}
                </div>
                <Avatar 
                    size={28}
                    src={getUserAvatar(data.id).src}
                />
            </Space>
        </Dropdown>
    )
}

export default User;