import {Drawer, DrawerProps} from 'antd';
import classNames from 'classnames';
import styles from './Drawer.module.scss';

const DrawerModule = (props: DrawerProps) => {
    return (
        <Drawer 
            {...props} 
            className={classNames(styles.drawer, props.className)}
        />
    )
}

export default DrawerModule;