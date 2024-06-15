import * as React from 'react';
import {UserOutlined, LogoutOutlined} from '@ant-design/icons';
import {Avatar, Menu} from 'antd';
import { getUserAvatar } from '@/Utils/User/getUserAvatar/getUserAvatar';
import {useUser} from '@/Hooks/User/useUser';
import {useLogout} from '@/Hooks/User/useLogout';
import styles from './UserMenu.module.scss';

const UserMenu = () => {
    const {data: user} = useUser();
    const logout = useLogout();
    if (!user) return null;
    return (
        <div className={styles.wrapper}>
            <div className={styles.user}>
                <Avatar 
                    src={getUserAvatar(user.id).src}
                    className={styles.avatar}
                    size={42}>
                    <UserOutlined />
                </Avatar>
                <div className={styles.userInfo}>
                    <div className={styles.name}>
                        {user.name}
                    </div>
                    <div className={styles.email}>
                        {user.email}
                    </div>
                </div>
            </div>
            <Menu 
                className={styles.menu}
                items={[
                    {
                        label: 'Выйти',
                        key: 'logout',
                        icon: <LogoutOutlined />,
                        className: styles.logout,
                        onClick: () => {
                            logout();
                        }
                    }
                ]}
            />
        </div>
    )
}

export default UserMenu;