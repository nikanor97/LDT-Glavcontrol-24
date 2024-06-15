import {Space, DatePicker, Button} from 'antd';
import { HiOutlineDownload } from "react-icons/hi";

const Controls = () => {
    return (
        <Space>
            <DatePicker 
                picker="quarter" 
                size="large"
                placeholder="Выберите квартал"
            />
            <Button 
                icon={<HiOutlineDownload />}
                size="large">
                Скачать excel
            </Button>
        </Space>
    )
}

export default Controls;