// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useContext } from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import AttachmentIcon from '@mui/icons-material/Attachment';
import CloseIcon from '@mui/icons-material/Close';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import { styled } from '@mui/material/styles';
import {
    useItemFinalizeListener, FILE_STATES,
    useItemProgressListener, BatchItem,
} from '@rpldy/uploady';
import { useTranslate } from 'react-admin';

import { SessionContext, SessionContextInterface } from '@/context';
import { truncateText } from '@/utils';
import { WithTooltip, CircularProgress } from '@/common';

const Root = styled(Box, {
    name: 'GFAttachment',
    slot: 'root',
})(() => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-start',
    flexGrow: 1,
}));

const StyledBox = styled(Box, {
    name: 'GFAttachment',
    slot: 'content',
})(() => ({
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
}));

const StyledTypography = styled(Typography, {
    name: 'GFAttachment',
    slot: 'title',
})(({ theme }) => ({
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
}));

type AttachmentProps = object;

const Attachment: FC<AttachmentProps> = () => {
    const {
        attachedFile,
        setAttachedFile,
    } = useContext<SessionContextInterface>(SessionContext);

    const attachedFileId = attachedFile?.id || undefined;

    const { completed } = useItemProgressListener(attachedFileId) || { completed: 0 };
    const translate = useTranslate();

    useItemFinalizeListener((it: BatchItem) => {
        if (attachedFile) {
            setAttachedFile({
                ...attachedFile,
                state: it.state,
            });
        }
    }, attachedFileId);

    if (!attachedFile || !attachedFile.id) {
        return null;
    }

    const isSuccess = attachedFile.state === FILE_STATES.FINISHED;
    const isFinished = ![FILE_STATES.PENDING, FILE_STATES.UPLOADING].includes(
        attachedFile.state
    );

    const handleRemoveAttachment = (): void => {
        if (attachedFile) {
            setAttachedFile(undefined);
        }
    }

    return (
        <Root>
            <AttachmentIcon fontSize='small' />
            <StyledBox
                title={attachedFile.file.name}
            >
                <StyledTypography
                    variant='caption'
                >
                    {
                        `${truncateText(attachedFile.file.name, 17, 'characters')}`
                    }
                </StyledTypography>
                <WithTooltip
                    title={translate('ra.action.remove')}
                    trigger={(
                        <IconButton
                            edge='start'
                            aria-label={translate('ra.action.remove')}
                            disabled={!attachedFile}
                            onClick={handleRemoveAttachment}
                            size='small'
                        >
                            <CloseIcon />
                        </IconButton>
                    )}
                    arrow
                />
                {!isFinished && completed !==0 && <CircularProgress value={completed} /> }
                {isSuccess && <CheckCircleOutlineIcon color='success' />}
            </StyledBox>
        </Root>
    );
}

export default Attachment;
