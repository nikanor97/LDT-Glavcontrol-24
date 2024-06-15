import {Button, Space, Upload} from 'antd';
import { HiOutlineDownload } from "react-icons/hi";
import { HiOutlineUpload } from "react-icons/hi";
import {useUploadExcel} from '@/Hooks/Procurements/useUploadExcel';

const Controls = () => {
    const uploadExcel = useUploadExcel();
    return (
        <Space 
            size={16}
            direction='horizontal'>
            <Button 
                icon={<HiOutlineDownload />}
                size="large">
                Скачать xlsx
            </Button>
            <Upload     
                multiple={false}
                customRequest={(options) => {
                    if (typeof options.file === 'string') return;
                    uploadExcel.mutate(options.file)
                }}
                showUploadList={false}>
                <Button 
                    icon={<HiOutlineUpload />}
                    disabled={uploadExcel.isPending}
                    size="large">
                    Загрузить xlsx
                </Button>
            </Upload>
            
        </Space>
    )
}

export default Controls;