import classnames from 'classnames';
import styles from './PageTitle.module.scss';

type iPageTitle = {
    children: React.ReactNode;
    className?: string;
}

const PageTitle = (props: iPageTitle) => {
    return (
        <div className={classnames(styles.wrapper, props.className)}>
            {props.children}
        </div>
    )
}


export default PageTitle