import {RuleObject} from "antd/lib/form";

export const required = (name?:string, nameOnly?: boolean):RuleObject => {
    return {
        required: true,
        message: nameOnly
            ? name
            : `Поле ${name || ''} обязательно для заполнения`
    };
};