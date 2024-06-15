import styles from './Company.module.scss';
import {Row, Col, Space, Avatar} from 'antd';
import CompanyField from './Components/CompanyField/CompanyField';
import StateController from '@/Containers/StateController/StateController';
import {useMyCompany} from '@/Hooks/Company/useMyCompany';
import { HiMap, HiCalendarDays } from "react-icons/hi2";

import { getUserAvatar } from '@/Utils/User/getUserAvatar/getUserAvatar';
import dayjs from 'dayjs';


const Company = () => {
    const {data: company, isLoading, isError} = useMyCompany();
    return (
        <div className={styles.wrapper}>
            <div className={styles.title}>
                О компании
            </div>
            <StateController 
                state={{
                    isLoading,
                    isError,
                    isEmpty: company === null
                }}
                data={company}>
                {
                    company && (
                        <Row gutter={[24,24]}>
                            <Col span={8}>
                                <CompanyField 
                                    title="Наименование"
                                    value={company.name}
                                />
                            </Col>
                            <Col span={8}>
                                <CompanyField 
                                    title="Регион"
                                    value={
                                        <Space 
                                            size={8}
                                            direction="horizontal">
                                            <HiMap />
                                            {company.region}
                                        </Space>
                                    }
                                />
                            </Col>
                            <Col span={8}>
                                <CompanyField 
                                    title="ИНН"
                                    value={company.inn}
                                />
                            </Col>
                            <Col span={8}>
                                <CompanyField 
                                    title="Директор"
                                    value={
                                        <Space 
                                            size={8}
                                            direction="horizontal">
                                            <Avatar 
                                                size={20}
                                                src={getUserAvatar(company.director).src}
                                            />
                                            {company.director}
                                        </Space>
                                    }
                                />
                            </Col>
                            <Col span={8}>
                                <CompanyField 
                                    title="Дата основания"
                                    value={
                                        <Space 
                                            size={8}
                                            direction="horizontal">
                                            <HiCalendarDays />
                                            {dayjs(company.foundation_date, {format: 'YYYY-MM-DD'}).format('DD MMMM YYYY')}
                                        </Space>
                                    }
                                />
                            </Col>
                            <Col span={8}>
                                <CompanyField 
                                    title="ОГРН"
                                    value={company.ogrn}
                                />
                            </Col>
                        </Row>
                    )
                }
            </StateController>
        </div>
    )
}


export default Company;