import {Select, SelectProps} from 'antd';
import {useCompanies} from '@/Hooks/Company/useCompanies';

const CompanySelect = (props: SelectProps) => {
    const {data, isLoading} = useCompanies({offset: 0, limit: 1000})
    return (
        <Select 
            {...props}
            loading={isLoading}
            options={data && data.items.map((item) => ({
                label: item.name,
                value: item.id
            }))}
        />
    )
}

export default CompanySelect;