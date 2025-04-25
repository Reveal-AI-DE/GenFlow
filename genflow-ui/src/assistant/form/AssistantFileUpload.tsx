// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC,useMemo, useContext } from 'react';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import {
    useRecordContext, useTranslate, useRefresh,
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
    if (!assistant) {
        return null;
    }

    const translate = useTranslate();
    const refresh = useRefresh();
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
                case FILE_STATES.ABORTED:
                    setRemainingFiles((prevItemCount) => (prevItemCount - 1));
                    break;
                default:
                    break;
            }
        },
    }), []);

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
