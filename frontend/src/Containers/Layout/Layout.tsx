import {App} from '@/Types';
import DefaultLayout from '@/Layouts/Default/Default';

type iLayout = Pick<App.Next.NextPage, 'getLayout'> & {
    children: React.ReactElement;
};

const defaultLayout: App.Next.NextPage['getLayout'] = (content) => {
    return (
        <DefaultLayout>
            {content}
        </DefaultLayout>
    )
}

const LayoutController = (props: iLayout) => {
    const layoutFunc = props.getLayout || defaultLayout;
    return layoutFunc(props.children) 
}

export default LayoutController;