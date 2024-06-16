import Loader from '@/Components/Loader/Loader'
import {Alert, Empty} from 'antd';
import {isArray} from 'lodash';
import styles from './StateController.module.scss';
import classnames from 'classnames';

type iStateController = {
    state?: {
        isLoading?: boolean;
        isError?: boolean;
        isEmpty?: boolean;
    }
    data: unknown;
    loaderFullHeight?: boolean;
    components?: {
        loading?: React.ReactNode;
        error?: React.ReactNode;
        empty?: React.ReactNode;
    }
    children: React.ReactNode;
}

const StateController = (props: iStateController) => {
    const {state, components} = props;
    const loadingCmp = components?.loading || (
        <div className={classnames(styles.loader, {
            [styles.loaderFullHeight]: props.loaderFullHeight
        })}>
            <Loader text="Загрузка данных..." />
        </div>
    )
    const errorCmp = components?.error || <Alert type="error" message="Ошибка при загрузке данных" />
    const emptyCmp = components?.empty || <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="Данные отсутствуют" />

    if (state?.isError) return errorCmp;
    if (state?.isLoading) return loadingCmp;
    if (state?.isEmpty !== undefined) {
        //empty задан напрямую
        if (state?.isEmpty) return emptyCmp;
    } else {
        //empty не задан проверим данные
        if (isArray(props.data)) {
            if (!props.data.length) return emptyCmp;
        }
    }
    return props.children;
}

export default StateController;