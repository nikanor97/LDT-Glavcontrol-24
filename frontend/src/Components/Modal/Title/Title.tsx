import classnames from 'classnames';
import styles from './Title.module.scss';

type iModalTitle = {
    children: React.ReactNode;
    className?: string;
}

const ModalTitle = (props: iModalTitle) => {
    return (
        <div className={classnames(styles.wrapper, props.className)}>
            {props.children}
        </div>
    )
}

export default ModalTitle;