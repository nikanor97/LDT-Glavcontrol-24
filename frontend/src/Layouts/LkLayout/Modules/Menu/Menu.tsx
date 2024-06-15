import {data} from './Data/Menu';
import MenuItem from './Components/MenuItem/MenuItem';
import {Row, Col} from 'antd';
import {iMenuItem} from './types';

type iMenu = {
    items: iMenuItem[];
}

const Menu = (props: iMenu) => {
    return (
        <Row gutter={[8, 8]}>
            {
                props.items.map((item, index) => (
                    <Col 
                        key={index}
                        span={24}>
                        <MenuItem 
                            item={item}
                        />
                    </Col>
                ))
            }
        </Row>
    )
}

export default Menu;