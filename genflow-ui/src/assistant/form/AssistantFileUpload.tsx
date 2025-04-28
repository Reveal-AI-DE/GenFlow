// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC,useMemo, useContext } from 'react';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import {
    useRecordContext, useTranslate,
    useRefresh, useNotify,
} from 'react-admin';
import {
    UPLOADER_EVENTS, Batch,
    BatchItem, FILE_STATES,
} from '@rpldy/uploady';

import { Assistant } from '@/types';
import { AssistantContext, AssistantContextInterface } from '@/context';
import { UploadArea } from '@/common';
import { createUploadyDestination } from '@/utils';
import { FileList } from '@/file';

type AssistantFilesUploadProps = object;

const AssistantFileUpload: FC<AssistantFilesUploadProps> = () => {
    const assistant = useRecordContext<Assistant>()
    const translate = useTranslate();
    const refresh = useRefresh();
    const notify = useNotify();
    const { setRemainingFiles } = useContext<AssistantContextInterface>(AssistantContext);

    const listeners = useMemo(() => ({
        [UPLOADER_EVENTS.BATCH_ADD]: (batch: Batch) => {
            setRemainingFiles((prevItemCount) => (prevItemCount + batch.items.length));
        },
        [UPLOADER_EVENTS.ITEM_FINALIZE]: (item: BatchItem) => {
            switch (item.state) {
                case FILE_STATES.FINISHED:
                    setRemainingFiles((prevItemCount) => (prevItemCount - 1));
                    refresh();
                    break;
                case FILE_STATES.ERROR: {
                    const message = item.uploadResponse?.data?.message;
                    if (Array.isArray(message)) {
                        notify(message[0], { type: 'error' });
                    } else if (typeof message === 'string') {
                        notify(message, { type: 'error' });
                    } else {
                        notify('ra.notification.http_error', { type: 'error' });
                    }
                    setRemainingFiles((prevItemCount) => (prevItemCount - 1));
                    refresh();
                    break;
                }
                case FILE_STATES.ABORTED:
                    setRemainingFiles((prevItemCount) => (prevItemCount - 1));
                    break;
                default:
                    break;
            }
        },
    }), []);

    if (!assistant) {
        return null;
    }

    const destination = createUploadyDestination('assistants', assistant.id);

    return (
        <>
            <UploadArea
                autoUpload={false}
                destination={destination || undefined}
                dropZoneOptions={{
                    accept: {
                        'text/plain': ['.txt'],
                        'text/html': ['.html', '.htm'],
                        'application/pdf': ['.pdf']
                    },
                    multiple: true,
                }}
                listeners={listeners}
            />
            <Divider sx={{m: 1}} />
            <Typography
                variant='subtitle1'
                component='span'
            >
                {translate('label.assistant.files')}
            </Typography>
            <FileList
                resource='assistants'
                recordId={assistant.id}
            />
        </>
    );
};

export default AssistantFileUpload;
