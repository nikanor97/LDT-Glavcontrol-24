import React, {useMemo} from 'react';
import styles from './Default.module.scss';

type iDefault = {
    children: React.ReactNode;
}

const Default = (props: iDefault) => {
    return (
        <div className={styles.wrapper}>
            {props.children}
        </div>
    );
};

export default Default;