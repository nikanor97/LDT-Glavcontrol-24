import {Modal} from 'antd';
import styles from './DeleteModal.module.scss';
import {usePrivateStore} from '../../Store/Store';
import ModalTitle from '@/Components/Modal/Title/Title';

const DeleteModal = () => {
    const closeModal = usePrivateStore((state) => state.actions.closeDeleteModal);
    const visible = usePrivateStore((state) => state.deleteModal.visible);
    const item = usePrivateStore((state) => state.deleteModal.item);
    return (
        <Modal 
            okText="Подтвердить"
            cancelText="Отмена"
            okButtonProps={{
                loading: true
            }}
            onClose={closeModal}
            open={visible}>
            <ModalTitle>
                Подтвердите удаление заявки
            </ModalTitle>
            <div className={styles.content}>
                <div className={styles.desc}>
                    Вы выбрали заявку для удаления.
                    После удаления изменения нельзя будет вернуть
                </div>
            </div>
        </Modal>
    )
}

export default DeleteModal;