import styles from './Company.module.scss';
import {Row, Col} from 'antd';
import {iCompany} from './types';
import CompanyField from './Components/CompanyField/CompanyField';
import StateController from '@/Containers/StateController/StateController';
import {useMyCompany} from '@/Hooks/Company/useMyCompany';


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
                        </Row>
                    )
                }
            </StateController>
        </div>
    )
}


export default Company;