import {Badge, BadgeProps} from 'antd';
import {Requests} from '@/Types';

type iStatus = {
    status: Requests.Status;
}

const getText = (status: Requests.Status) => {
    switch (status) {
        case 'draft':
            return 'Черновик'
        default:
            return 'Создан'
    }
}

const getStatus = (status: Requests.Status):BadgeProps['status'] => {
    switch (status) {
        case 'draft':
            return 'default'
        default:
            return 'success'
    }
}




const Status = (props: iStatus) => {
    return (
        <Badge 
            text={getText(props.status)} 
            status={getStatus(props.status)}
        />
    )
}

export default Status;