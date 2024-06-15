import React from 'react';
import styles from './ErrorBoundary.module.scss';

interface iErrorBoundary {
    children: any;
}
interface HocState {
    hasError: boolean;
}
class ErrorBoundary extends React.Component<iErrorBoundary> {
    constructor(props: iErrorBoundary) {
        super(props);
        this.state = {hasError: false};
    }

    readonly state: HocState = {
        hasError: false
    };

    static getDerivedStateFromError() {
        // Обновить состояние с тем, чтобы следующий рендер показал запасной UI.
        return {hasError: true};
    }

    async componentDidCatch(error: Error | null, info: object) {
        // Можно также сохранить информацию об ошибке в соответствующую службу журнала ошибок
        console.log(error,info);
    }

    render() {
        if (this.state.hasError) {
            // Можно отрендерить запасной UI произвольного вида
            return (
                <div className={styles.wrapper}>
                    К сожалению, произошла ошибка в работе приложения :( <br />
                    Пожалуйста, свяжитесь с нами и опишите вашу проблему, чтобы мы могли скорее вам помочь.
                </div>
            )
        }
        return this.props.children;
    }
}

export default ErrorBoundary;