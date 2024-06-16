import styles from './ContentInfo.module.scss';


type iContentInfo = {
    title: React.ReactNode;
    content: React.ReactNode
}

const ContentInfo = (props: iContentInfo) => {
    return (
        <div className={styles.wrapper}>
            <div className={styles.title}>
                {props.title}
            </div>
            <div className={styles.desc}>
                {props.content}
            </div>
        </div>
    )
}

export default ContentInfo;