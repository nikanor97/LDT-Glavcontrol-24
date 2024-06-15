import {iMenuItem} from '../../types';
import styles from './MenuItem.module.scss';
import Link from 'next/link'
import {useIsActive} from './Hooks/useIsActive';
import classnames from 'classnames';

type iMenuItemProps = {
    item: iMenuItem
}

const MenuItem = (props: iMenuItemProps) => {
    const {item} = props;
    const isActive = useIsActive(item.link, item.exact);
    return (
        <Link 
            href={item.link}
            className={classnames(styles.wrapper, {
                [styles.active]: isActive
            })}>
            <div className={styles.icon}>
                {item.icon}
            </div>
            {item.text}
        </Link>
    )
}


export default MenuItem;