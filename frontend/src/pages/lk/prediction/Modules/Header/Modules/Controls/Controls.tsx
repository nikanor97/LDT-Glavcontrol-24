import {Space, DatePicker, Button} from 'antd';
import { HiOutlineDownload } from "react-icons/hi";
import {usePrivateStore} from '../../../../Store/Store';
import dayjs from 'dayjs';


const Controls = () => {
    const changeParams = usePrivateStore((state) => state.actions.changeParams);
    return (
        <Space>
            <DatePicker 
                picker="quarter" 
                size="large"
                defaultValue={dayjs()}
                placeholder="Выберите квартал"
                onChange={(date) => {
                    changeParams({
                        quarter: date.quarter(),
                        year: date.year(),
                        offset: 0
                    })
                }}
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