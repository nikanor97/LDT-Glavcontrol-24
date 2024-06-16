import {Button, Space, Upload, notification} from 'antd';
import { HiOutlineDownload } from "react-icons/hi";
import { HiOutlineUpload } from "react-icons/hi";
import {useUploadExcel} from '@/Hooks/Procurements/useUploadExcel';
import {queryKey} from '@/Hooks/Procurements/useProcurements';
import {useQueryClient} from '@tanstack/react-query';
import NotificationContent from '@/Components/Notification/ContentInfo/ContentInfo';
import {nanoid} from 'nanoid';

const Controls = () => {
    const uploadExcel = useUploadExcel();
    const client = useQueryClient();
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
                    const id = nanoid();
                    notification.info({
                        key: `order_upload:${id}`,
                        message: (
                            <NotificationContent 
                                title="Загружаем закупки"
                                content="Выполняется загрузка файла с закупками..."
                            />
                        )
                    })
                    uploadExcel.mutate(options.file, {
                        onSuccess: () => {
                            notification.success({
                                key: `order_upload:${id}`,
                                message: (
                                    <NotificationContent 
                                        title="Закупки успешно загружены"
                                        content="Мы загрузили файл с закупками и обновили данные"
                                    />
                                )
                            })
                            client.resetQueries({
                                queryKey
                            })
                        },
                        onError: (ex) => {
                            notification.error({
                                key: `order_upload:${id}`,
                                message: (
                                    <NotificationContent 
                                        title="Ошибка при загрузке файла закупок"
                                        content="При загрузке файла возникла ошибка. Пожалуйста, обратитесь в поддержку для решения проблемы"
                                    />
                                )
                            })
                        }
                    })
                    
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