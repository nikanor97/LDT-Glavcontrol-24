import styles from './Block.module.scss';

type iBlock = {
    children: React.ReactNode;
    title: React.ReactNode;
}

const Block = (props: iBlock) => {
    return (
        <div className={styles.wrapper}>
            <div className={styles.title}>
                {props.title}
            </div>
            {props.children}
        </div>
    )
}

export default Block;