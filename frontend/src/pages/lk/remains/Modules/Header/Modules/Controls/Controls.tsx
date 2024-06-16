import {Space, Button} from 'antd';
import { HiOutlineDownload } from "react-icons/hi";
import { HiOutlineUpload } from "react-icons/hi";
import Routes from '@/Routes/Routes';
import {useUser} from '@/Hooks/User/useUser';

const Controls = () => {
    const {data: user} = useUser();
    if (!user) return null;
    return (
        <Space 
            size={16}
            direction='horizontal'>
            <a 
                download="remains.xlsx"
                href={Routes.api.remainsExportExcel(user.id)}>
                <Button 
                    icon={<HiOutlineDownload />}
                    size="large">
                    Скачать excel
                </Button>
            </a>
            <Button 
                type="primary"
                icon={<HiOutlineUpload />}
                size="large">
                Загрузить
            </Button>
        </Space>
    )
}

export default Controls;