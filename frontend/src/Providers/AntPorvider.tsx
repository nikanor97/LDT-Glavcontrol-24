import { PropsWithChildren } from "react"
import {ConfigProvider, notification} from 'antd';


type iAntPropvider = PropsWithChildren;

notification.config({
    showProgress: true,
    closable: true
})

const AntProvider = (props: iAntPropvider) => {
    return (
        <ConfigProvider theme={{
            components: {
                Form: {
                    verticalLabelPadding: '4px',
                    itemMarginBottom: 16,
                    labelRequiredMarkColor: 'inherit',
                },
                Button: {
                    defaultBg: '#E4E7EC',
                    defaultBorderColor: 'transparent',
                    defaultColor: '#101828',
                    defaultHoverBg: '#E4E7EC',
                    defaultHoverColor: '#000',
                    defaultHoverBorderColor: 'transparent'
                }
            },
            token: {
                colorPrimary: '#D92D20',
                colorPrimaryHover: '#b02116',
            },
        }}>
            {props.children}
        </ConfigProvider>
    )
}

export default AntProvider;