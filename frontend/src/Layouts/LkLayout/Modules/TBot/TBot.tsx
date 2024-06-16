import styles from './TBot.module.scss';
import Image from 'next/image'
import btn from './Images/btn.png';
import {useBotStore} from '@/Zustand/BotModal/BotModal';

const TBot = () => {
    const openModal = useBotStore((state) => state.actions.openModal);
    return (
        <div 
            onClick={() => openModal()}
            className={styles.wrapper}>
            <div className={styles.content}>
                <div className={styles.title}>
                    Готовые прогнозы под рукой
                </div>
                <div className={styles.desc}>
                    Используйте чат-бот для мобильного прогнозирования
                </div>
            </div>
            <div className={styles.btn}>
                <Image 
                    alt="btn"
                    src={btn}
                />
            </div>
            <div className={styles.background} />
        </div>
    )
}

export default TBot;