import classNames from 'classnames';
import styles from './BlockTitle.module.scss';
import { HiChevronRight } from "react-icons/hi";


type iBlockTitle = {
    children: React.ReactNode;
    className?: string;
}

const BlockTitle = (props: iBlockTitle) => {
    return (
        <div className={classNames(styles.wrapper, props.className)}>
            {props.children}
            <span className={styles.icon}>
                <HiChevronRight />
            </span>
        </div>
    )
}

export default BlockTitle;