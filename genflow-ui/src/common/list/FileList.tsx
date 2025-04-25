// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import Typography from '@mui/material/Typography';
import { useTranslate } from 'react-admin';

import { FileEntity } from '@/types';
import { truncateText } from '@/utils';

interface FileItemProps {
    item: FileEntity;
};

const FileItem: FC<FileItemProps> = ({
    item,
}) => (
    <ListItem
        secondaryAction={(
            <IconButton
                edge='end'
                aria-label='delete'
            >
                <DeleteIcon
                    fontSize='small'
                    color='error'
                />
            </IconButton>
        )}
    >
        <ListItemIcon>
            <InsertDriveFileIcon fontSize='small' />
        </ListItemIcon>
        <ListItemText
            title={item.id as string}
            secondary={truncateText(item.id as string, 50, 'characters')}
        />
    </ListItem>
);

interface FileListProps {
    items: FileEntity[];
};

const FileList: FC<FileListProps> = ({
    items,
}) => {
    const translate = useTranslate();

    return (items.length > 0 ? (
        <List
            dense
        >
            {
                items.map((item: any) => (
                    <FileItem
                        key={item.id}
                        item={item}
                    />
                ))
            }
        </List>
    ) : (
        <Typography variant='body2'>
            {translate('label.assistant.no_files')}
        </Typography>
    ));
}

export default FileList;
