// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useContext, useState } from 'react';
import InputAdornment from '@mui/material/InputAdornment';
import { useTranslate, useRecordContext } from 'react-admin';
import Uploady, { UploadyProps } from '@rpldy/uploady';

import { SessionContext, SessionContextInterface } from '@/context';
import { Session } from '@/types';
import { useChatHandler } from '@/hook';
import { TextareaAutosize } from '@/common';
import { createUploadyDestination } from '@/utils';

import SendButton from '@/chat/form/input/SendButton';
import AttachButton from '@/chat/form/input/AttachButton';
import Attachment from '@/chat/form/input/Attachment';
import PromptSelection, { PromptSelectionButton } from './PromptSelection';

type ChatInputProps = UploadyProps

const ChatInput: FC<ChatInputProps> = ({
    ...props
}) => {
    const session = useRecordContext<Session>();

    const translate = useTranslate();

    const [, setIsTyping] = useState<boolean>(false)

    const {
        userInput,
        setUserInput,
    } = useContext<SessionContextInterface>(SessionContext);
    const { chatInputRef } = useChatHandler();

    const handleInputChange = (value: string): void => {
        setUserInput(value);
    }

    const destination = session ? createUploadyDestination('sessions', session.id) : undefined;

    return (
        <Uploady
            {...props}
            multiple={false}
            autoUpload={false}
            clearPendingOnAdd
            accept='text/plain,text/html,application/pdf'
            destination={destination || undefined}
        >
            <PromptSelection />
            <Attachment />
            <TextareaAutosize
                formControlProps={{
                    disabled: !session,
                    sx: { width: '100%' },
                }}
                inputProps={{
                    ref: chatInputRef,
                    minRows: 1,
                    maxRows: 4,
                    placeholder: translate('label.ask'),
                    value: userInput,
                    onCompositionStart: () => setIsTyping(true),
                    onCompositionEnd: () => setIsTyping(false),
                    onChange: (e) => handleInputChange(e.target.value),
                    startAdornment: (
                        <InputAdornment
                            position='start'
                            sx={{
                                marginTop: '0 !important'
                            }}
                        >
                            <PromptSelectionButton />
                            <AttachButton />
                        </InputAdornment>
                    ),
                    endAdornment: (
                        <InputAdornment position='end'>
                            <SendButton />
                        </InputAdornment>
                    )
                }}
            />
        </Uploady>
    );
};

export default ChatInput;
