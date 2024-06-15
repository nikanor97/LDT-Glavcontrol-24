import {Space, Button} from 'antd';
import getRoute from '@/Routes/Routes';
import Link from 'next/link';

const Controls = () => {
    return (
        <Space 
            size={16}
            direction='horizontal'>
            <Link href={getRoute.lk.createRequest}>
                <Button 
                    type="primary"
                    size="large">
                    Новая заявка
                </Button>
            </Link>
        </Space>
    )
}

export default Controls;