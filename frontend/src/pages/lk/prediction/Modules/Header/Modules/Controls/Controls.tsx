import {useMemo} from 'react';
import {Space, DatePicker, Button} from 'antd';
import { HiOutlineDownload } from "react-icons/hi";
import {usePrivateStore} from '../../../../Store/Store';
import styles from './Controls.module.scss';
import { declinationOfNumber } from '@/Utils/Normalize/declinationOfNumber';
import {useCreateRequestByPredicitions} from '@/Hooks/Requests/useCreateRequestByPredictions';
import { useDateByQuarter } from '@/Hooks/Date/useDateByQuarter';


const Controls = () => {
    const changeParams = usePrivateStore((state) => state.actions.changeParams);
    const setSelected = usePrivateStore((state) => state.actions.setSelected);
    const selected = usePrivateStore((state) => state.selected);
    const params = usePrivateStore((state) => state.params);
    const createRequest = useCreateRequestByPredicitions();
    const value = useDateByQuarter(params.quarter, params.year);
    return (
        <Space>
            {
                Boolean(selected.length) && (
                    <>
                        <div className={styles.choosen}>
                            Выбрано: {
                                declinationOfNumber({
                                    value: selected.length,
                                    words: ['объект', 'объекта', 'объектов']
                                })
                            }
                        </div>
                        <Button 
                            loading={createRequest.isPending}
                            onClick={() => {
                                createRequest.mutate({
                                    forecast_ids: selected
                                });
                            }}
                            size="large"
                            type="primary">
                            Создать заявку
                        </Button>
                    </>
                )
            }
            <DatePicker 
                picker="quarter"
                value={value}
                size="large"
                placeholder="Выберите квартал"
                onChange={(date) => {
                    changeParams({
                        quarter: date.quarter(),
                        year: date.year(),
                        offset: 0
                    })
                    if (selected) setSelected([]);

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