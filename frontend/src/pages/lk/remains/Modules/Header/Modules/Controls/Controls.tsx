import {Space, Button} from 'antd';
import { HiOutlineDownload } from "react-icons/hi";
import { HiOutlineUpload } from "react-icons/hi";

const Controls = () => {
    return (
        <Space 
            size={16}
            direction='horizontal'>
            <Button 
                icon={<HiOutlineDownload />}
                size="large">
                Скачать excel
            </Button>
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