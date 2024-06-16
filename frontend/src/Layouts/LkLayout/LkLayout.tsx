import React from "react";
import Header from './Modules/Header/Header';
import styles from './LkLayout.module.scss';
import {Affix} from 'antd';
import TBot from './Modules/TBot/TBot';
import BotModal from "./Modules/BotModal/BotModal";
export {type iMenuItem} from './Modules/Menu/types';
export {default as Menu} from './Modules/Menu/Menu';

type iUserLayout = {
    children: React.ReactNode;
    menu: React.ReactNode;
}

const UserLayout = (props: iUserLayout) => {
    return (
        <div className={styles.wrapper}>
            <Header />
            <div className={styles.body}>
                <Affix>
                    <div className={styles.menu}>
                        {props.menu}
                        <div className={styles.bot}>
                            <TBot />
                        </div>
                        <BotModal />
                    </div>
                </Affix>
                <div className={styles.content}>
                    {props.children}
                </div>
            </div>
        </div>
    )
}


export default UserLayout;