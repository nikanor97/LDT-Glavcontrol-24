import styles from './Remains.module.scss';
import Header from './Modules/Header/Header';
import {useRemainsStats} from '@/Hooks/Company/useRemainsStats';
import StateController from '@/Containers/StateController/StateController';
import {usePrivateStore} from '../../Store/Store';
import Graphic from './Modules/Graphic/Graphic';

const Remains = () => {
    const {quarter, year} = usePrivateStore((state) => state.remains);
    const {data, isLoading, isError} = useRemainsStats({quarter, year})
    return (
        <div className={styles.wrapper}>
            <Header />
            <div className={styles.content}>
                <StateController 
                    state={{isError, isLoading}}
                    data={data}>
                    <Graphic />
                </StateController>
            </div>
        </div>
    )
}


export default Remains;