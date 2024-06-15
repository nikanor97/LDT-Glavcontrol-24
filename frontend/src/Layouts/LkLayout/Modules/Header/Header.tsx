import styles from './Header.module.scss';
import Image from 'next/image';
import Logo from '@/Img/logo.png';
import User from './Modules/User/User';


const Header = () => {
    return (
        <header className={styles.wrapper}>
            <div>
                <Image 
                    className={styles.logo}
                    src={Logo}
                    alt="logo"
                />
            </div>
            <User />
        </header>
    )
}

export default Header;