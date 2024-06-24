import {Space, DatePicker, Button, Select} from 'antd';
import { HiOutlineDownload } from "react-icons/hi";
import {usePrivateStore} from '../../../../Store/Store';
import styles from './Controls.module.scss';
import { declinationOfNumber } from '@/Utils/Normalize/declinationOfNumber';
import {useCreateRequestByPredicitions} from '@/Hooks/Requests/useCreateRequestByPredictions';
import { useDateByQuarter } from '@/Hooks/Date/useDateByQuarter';
import {Routes} from '@/Routes/Routes';
import { useUser } from '@/Hooks/User/useUser';
import {usePredictions} from '../../../../Hooks/usePredictions';

const Controls = () => {
    const changeParams = usePrivateStore((state) => state.actions.changeParams);
    const setSelected = usePrivateStore((state) => state.actions.setSelected);
    const selected = usePrivateStore((state) => state.selected);
    const params = usePrivateStore((state) => state.params);
    const createRequest = useCreateRequestByPredicitions();
    const value = useDateByQuarter(params.quarter, params.year);
    const {data} = usePredictions();

    const {data: user} = useUser();
    if (!user) return null;
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
            {
                Boolean(data?.items.length) && (
                    <a 
                        download="forecast.json"
                        href={Routes.api.predictionsExportJSON(params.year, user.id, params.quarter)}>
                        <Button 
                            icon={<HiOutlineDownload />}
                            size="large">
                            Скачать JSON
                        </Button>
                    </a>
                )
            }
            <Select<number | undefined> 
                value={params.quarter}
                placeholder="Выбор квартала"
                onChange={(value) => {
                    changeParams({
                        quarter: value
                    })
                }}
                style={{
                    minWidth: 150
                }}
                allowClear
                size="large">
                <Select.Option value={1}>
                    Q1
                </Select.Option>
                <Select.Option value={2}>
                    Q2
                </Select.Option>
                <Select.Option value={3}>
                    Q3
                </Select.Option>
                <Select.Option value={4}>
                    Q4
                </Select.Option>
            </Select>
            <DatePicker 
                picker="year"
                value={value}
                size="large"
                placeholder="Выберите год"
                disabledDate={(date) => {
                    return date.year() !== 2023
                }}
                onChange={(date) => {
                    changeParams({
                        year: date.year(),
                        quarter: undefined,
                        offset: 0
                    })
                    if (selected) setSelected([]);
                }}
            />
            <a 
                download="forecast.xlsx"
                href={Routes.api.predictionsExportExcel(params.year, user.id, params.quarter)}>
                <Button 
                    icon={<HiOutlineDownload />}
                    size="large">
                Скачать excel
                </Button>
            </a>
        </Space>
    )
}

export default Controls;