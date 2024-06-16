import {Modal, Button} from 'antd';
import {useBotStore} from '@/Zustand/BotModal/BotModal';
import Image from 'next/image';
import qrImage from './Images/qr.png';
import styles from './BotModal.module.scss';

const BotModal = () => {
    const visible = useBotStore((state) => state.visible);
    const closeModal = useBotStore((state) => state.actions.closeModal);
    return (
        <Modal 
            title="Открыть чат бот"
            onClose={() => closeModal()}
            onCancel={() => closeModal()}
            footer={false}
            width="400px"
            open={visible}>
            <div className={styles.wrapper}>
                <div className={styles.desc}>
                    Отсканируйте QR-код на мобильном устройстве или откройте в чат в браузере
                </div>
                <div className={styles.qrWrapper}>
                    <div className={styles.qr}>
                        <Image 
                            src={qrImage}
                            width={170}
                            height={170}
                            alt="qr"
                        />
                    </div>
                </div>
                <a 
                    href="https://t.me/DeepPeople_GlavControl_bot"
                    className={styles.link}>
                    <Button 
                        className={styles.btn}
                        size="large">
                        Открыть в браузере
                    </Button>
                </a>
            </div>
        </Modal>
    )
}

export default BotModal;