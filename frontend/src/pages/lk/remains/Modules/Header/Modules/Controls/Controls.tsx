import {Space, Button, Upload, notification} from 'antd';
import { HiOutlineDownload } from "react-icons/hi";
import { HiOutlineUpload } from "react-icons/hi";
import Routes from '@/Routes/Routes';
import {useUser} from '@/Hooks/User/useUser';
import NotificationContent from '@/Components/Notification/ContentInfo/ContentInfo';
import {nanoid} from 'nanoid';
import {useQueryClient} from '@tanstack/react-query';
import {useUploadExcel} from '@/Hooks/Remains/useUploadExcel';
import {getKey} from '@/Hooks/Remains/useRemains';

const Controls = () => {
    const {data: user} = useUser();
    const client = useQueryClient();
    const uploadExcel = useUploadExcel();

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
            <Upload     
                multiple={false}
                customRequest={(options) => {
                    if (typeof options.file === 'string') return;
                    const id = nanoid();
                    notification.info({
                        key: `remains_upload:${id}`,
                        message: (
                            <NotificationContent 
                                title="Загружаем остатки"
                                content="Выполняется загрузка файла с остатками..."
                            />
                        )
                    })
                    uploadExcel.mutate(options.file, {
                        onSuccess: () => {
                            notification.success({
                                key: `remains_upload:${id}`,
                                message: (
                                    <NotificationContent 
                                        title="Остатки успешно загружены"
                                        content="Мы загрузили файл с остатками и обновили данные"
                                    />
                                )
                            })
                            client.resetQueries({
                                queryKey: getKey
                            })
                        },
                        onError: (ex) => {
                            notification.error({
                                key: `remains_upload:${id}`,
                                message: (
                                    <NotificationContent 
                                        title="Ошибка при загрузке файла остатков"
                                        content="При загрузке файла возникла ошибка. Пожалуйста, обратитесь в поддержку для решения проблемы"
                                    />
                                )
                            })
                        }
                    })
                    
                }}
                showUploadList={false}>
                <Button 
                    type="primary"
                    disabled={uploadExcel.isPending}
                    icon={<HiOutlineUpload />}
                    size="large">
                    Загрузить
                </Button>
            </Upload>
            
        </Space>
    )
}

export default Controls;