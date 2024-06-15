import {Table as AntTable, TableProps} from 'antd';
import classnames from 'classnames';
import styles from './Table.module.scss';


const Table = (props: TableProps) => {
    return (
        <AntTable 
            {...props} 
            className={classnames(styles.table, props.className)}
        />
    )
}

export default Table;