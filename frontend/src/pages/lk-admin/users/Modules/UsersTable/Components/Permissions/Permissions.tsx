import { User } from "@/Types"
import { useMemo } from "react";
import styles from './Permissions.module.scss';
import { Tooltip } from "antd";


type iPermissions = {
    item: User.WithCompany;
}

const Permissions = (props: iPermissions) => {
    const {item} = props;
    const result = useMemo(() => {
        const permissions: string[] = []
        if (item.user_permission_create_order) permissions.push('создание заявок');
        if (item.user_permission_read_stat) permissions.push('просмотр статистики');
        if (permissions.length) return permissions.join(',')
        else return '-'
    }, [item]);
    return (
        <Tooltip title={result}>
            <div className={styles.wrapper}>
                {result}
            </div>
        </Tooltip>
    )
}

export default Permissions