// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    FC, useContext,
} from 'react';
import IconButton from '@mui/material/IconButton';
import SendIcon from '@mui/icons-material/Send';
import StopIcon from '@mui/icons-material/Stop';
import {
    useUploadyContext, useItemFinishListener,
    BatchItem, FILE_STATES, useItemErrorListener,
} from '@rpldy/uploady';
import { useTranslate, useNotify } from 'react-admin';

import { SessionContext, SessionContextInterface } from '@/context';
import { WithTooltip } from '@/common';
import { useChatHandler } from '@/hook';

type SendButtonProps = object;

const SendButton: FC<SendButtonProps> = () => {
    const translate = useTranslate();
    const notify = useNotify();

    const {
        userInput,
        isGenerating,
        attachedFile,
        userFiles,
        setUserFiles,
    } = useContext<SessionContextInterface>(SessionContext);

    const { processPending } = useUploadyContext();
    const {
        handleSendMessage,
        handleStopMessage
    } = useChatHandler();

    const onSendClick = (): void => {
        if (isGenerating) {
            handleStopMessage();
        }
        else {
            if (!userInput) return;
            if (attachedFile) {
                if (attachedFile.state === FILE_STATES.PENDING) {
                    processPending();
                } else {
                    handleSendMessage(
                        userInput,
                        userFiles
                    );
                }
            } else {
                handleSendMessage(userInput)
            }
        }
    };

    useItemFinishListener((it: BatchItem) => {
        const { data } = it.uploadResponse;
        const files = attachedFile ? [data] : []
        setUserFiles(files);
        handleSendMessage(
            userInput,
            files
        );
    }, attachedFile?.id);

    useItemErrorListener((item: BatchItem) => {
        const message = item.uploadResponse?.data?.message;
        if (Array.isArray(message)) {
            notify(message[0], { type: 'error' });
        } else if (typeof message === 'string') {
            notify(message, { type: 'error' });
        } else {
            notify('ra.notification.http_error', { type: 'error' });
        }
    }, attachedFile?.id);

    return (
        <WithTooltip
            title={translate('action.send')}
            trigger={(
                <span>
                    <IconButton
                        edge='end'
                        aria-label={isGenerating ? translate('action.stop') : translate('action.send')}
                        disabled={!userInput}
                        onClick={onSendClick}
                    >
                        {
                            isGenerating ? (
                                <StopIcon />
                            ) : (
                                <SendIcon />
                            )
                        }
                    </IconButton>
                </span>
            )}
            arrow
        />
    );
};

export default SendButton;
