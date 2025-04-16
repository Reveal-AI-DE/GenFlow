// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    FC, useContext, useCallback,
    useRef, SyntheticEvent,
} from 'react';
import IconButton from '@mui/material/IconButton';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import { useRecordContext, useTranslate } from 'react-admin';
import {
    useUploadyContext, UploadOptions,
    useBatchAddListener, Batch,
} from '@rpldy/uploady';

import { SessionContext, SessionContextInterface } from '@/context';
import { Session } from '@/types';
import { WithTooltip } from '@/common';

interface AttachButtonProps extends UploadOptions {
    onClick?: (e: SyntheticEvent<HTMLElement>) => void;
};

const AttachButton: FC<AttachButtonProps> = ({
    onClick,
    ...props
}) => {
    const session = useRecordContext<Session>();

    const translate = useTranslate();

    const { setAttachedFile } = useContext<SessionContextInterface>(SessionContext);
    const { showFileUpload } = useUploadyContext();

    // using ref so onButtonClick can stay memoized
    const uploadOptionsRef = useRef<UploadOptions>();
    // TODO: control allowed meta data
    uploadOptionsRef.current = {
        ...props,
        autoUpload: false,
        clearPendingOnAdd: true,
    };

    const handleClick = useCallback((e: SyntheticEvent<HTMLElement>) => {
        showFileUpload(uploadOptionsRef.current);
        onClick?.(e);
    }, [showFileUpload, uploadOptionsRef]);

    useBatchAddListener((batch: Batch) => {
        setAttachedFile(batch.items[0]);
    });

    return (
        <WithTooltip
            title={translate('action.attach')}
            trigger={(
                <span>
                    <IconButton
                        edge='start'
                        aria-label={translate('action.attach')}
                        disabled={!session}
                        onClick={handleClick}
                        size='small'
                    >
                        <AttachFileIcon
                            fontSize='small'
                        />
                    </IconButton>
                </span>
            )}
            arrow
        />
    );
};

export default AttachButton;
