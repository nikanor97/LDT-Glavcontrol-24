import styles from './CompanyField.module.scss';
import {iCompany} from '../../types';

type iCompanyField = {
    title: React.ReactNode;
    value: React.ReactNode;
}

const CompanyField = (props: iCompanyField) => {
    return (
        <div className={styles.wrapper}>
            <div className={styles.name}>
                {props.title}
            </div>
            <div className={styles.value}>
                {props.value}
            </div>
        </div>
    )
}


export default CompanyField;