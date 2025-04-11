// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useContext } from 'react';
import {
    useRecordContext, Form,
} from 'react-admin';

import {
    Session, SessionType, ChatModelSetting, ConfigurationType,
} from '@/types';
import { ConfigurableInputForm, ConfigurableInputProps } from '@/common';
import { SessionContext, SessionContextInterface } from '@/context';

type ChatSettingFormViewProps = object

const ChatSettingFormView: FC<ChatSettingFormViewProps> = () => {
    const session = useRecordContext<Session>();
    const { chatSetting, setChatSetting } = useContext<SessionContextInterface>(SessionContext);

    if (!session || !session.related_model || !session.related_model.entity.parameter_configs) {
        return null;
    }

    const chatModelSettings = chatSetting as ChatModelSetting;

    const onChange: ConfigurableInputProps['onChange'] = (value, config) => {
        const settings = {...chatModelSettings};
        if (config.type === ConfigurationType.INT) {
            const newValue = parseInt(value, 10);
            settings.parameters[config.name] = newValue;
        } else {
            settings.parameters[config.name] = value;
        }
        setChatSetting(settings)
    }

    return (
        <Form>
            <ConfigurableInputForm
                parameterConfigs={session.related_model.entity.parameter_configs}
                parameters={chatModelSettings.parameters}
                onChange={onChange}
            />
        </Form>
    )
};

type ChatSettingFormProps = object

const ChatSettingForm: FC<ChatSettingFormProps> = () => {
    const session = useRecordContext<Session>();

    if (
        !session ||
        (session.session_type === SessionType.LLM && !session.related_model) ||
        (session.session_type === SessionType.PROMPT && !session.related_prompt)
    ) {
        return null;
    }

    if (session.session_type === SessionType.LLM || session.session_type === SessionType.PROMPT) {
        return (
            <ChatSettingFormView />
        )
    }

    return null;
};

export default ChatSettingForm;
