// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import IconButton from '@mui/material/IconButton';
import BlockIcon from '@mui/icons-material/Block';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import {
    useItemFinalizeListener,
    useItemProgressListener,
    useAbortItem,
    FILE_STATES,
    BatchItem,
} from '@rpldy/uploady';

import { CircularProgress } from '@/common';
import { truncateText } from '@/utils';

interface UploadItemProps {
    item: BatchItem;
};

const UploadItem: FC<UploadItemProps> = ({
    item,
}) => {
    const [itemState, setState] = useState<FILE_STATES>(item.state);
    const abortItem = useAbortItem();
    const { completed } = useItemProgressListener(item.id) || { completed: 0 };

    useItemFinalizeListener((it: BatchItem) => {
        setState(it.state);
    }, item.id);

    const isAborted = itemState === FILE_STATES.ABORTED;
    const isSuccess = itemState === FILE_STATES.FINISHED;
    const isFinished = ![FILE_STATES.PENDING, FILE_STATES.UPLOADING].includes(
        itemState
    );

    const onAbortItem = (): void => {
        abortItem(item.id);
    };

    return (
        <ListItem
            secondaryAction={(
                <IconButton
                    edge='end'
                    aria-label='delete'
                    onClick={onAbortItem}
                >
                    <DeleteIcon fontSize='small' />
                </IconButton>
            )}
        >
            <ListItemIcon>
                {!isFinished && <CircularProgress value={completed} /> }
                {isAborted && <BlockIcon color='disabled' />}
                {isSuccess && <CheckCircleOutlineIcon color='success' />}
            </ListItemIcon>
            <ListItemText
                title={item.file.name}
                secondary={truncateText(item.file.name, 50, 'characters')}
                slotProps={{
                    secondary: {
                        color: isSuccess ? 'success' : 'textSecondary',
                        sx: {
                            textDecoration: isAborted ? 'line-through' : 'none',
                        }
                    },
                }}
            />
        </ListItem>
    )
};

export default UploadItem;
