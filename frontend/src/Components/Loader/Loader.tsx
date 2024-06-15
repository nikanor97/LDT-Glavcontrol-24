import styles from './Loader.module.scss';
import Logo from '@/Img/logo.png';
import Image from 'next/image'

type iLoader = {
    text: React.ReactNode;
}

const Loader = (props: iLoader) => {
    return (
        <div className={styles.wrapper}>
            <div className={styles.loader}>
                <Image 
                    alt="logo"
                    className={styles.logo}
                    src={Logo}
                />
            </div>
            <div className={styles.text}>
                {props.text}
            </div>
        </div>
    )
}


export default Loader;