// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useState } from 'react';
import List from '@mui/material/List';
import {
    useBatchAddListener,
    Batch, BatchItem, useUploadyContext
} from '@rpldy/uploady';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { TopToolbar, Button } from 'react-admin';

import UploadItem from '@/common/form/upload/UploadItem';

type UploadListProps = object;

const UploadList: FC<UploadListProps> = () => {
    const { processPending } = useUploadyContext();
    const [items, setItems] = useState<BatchItem[]>([]);

    useBatchAddListener((batch: Batch) => {
        setItems(() => items.concat(batch.items));
    });

    return (
        <>
            <List
                dense
            >
                {
                    items.map((item: any) => (
                        <UploadItem
                            key={item.id}
                            item={item}
                        />
                    ))
                }
            </List>
            {
                items.length > 0 && (
                    <TopToolbar>
                        <Button
                            label='action.upload'
                            startIcon={<UploadFileIcon />}
                            variant='outlined'
                            onClick={() => processPending()}
                        />
                    </TopToolbar>
                )
            }
        </>
    );
};

export default UploadList;
