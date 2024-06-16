import styles from './Layout.module.scss';

type iLayout = {
    children: React.ReactNode;
}

const Layout = (props: iLayout) => {
    return (
        <div className={styles.wrapper}>
            {props.children}
        </div>
    )
}


export default Layout;