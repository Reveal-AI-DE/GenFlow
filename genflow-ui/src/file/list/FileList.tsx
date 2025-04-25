// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    ListBase, Datagrid, Identifier,
    BulkDeleteWithConfirmButton,
} from 'react-admin';

import { FileField } from '@/file/show';

interface FileListProps {
    resource: string;
    recordId: Identifier;
};

const FileBulkActionButtons: FC<FileListProps> = ({
    resource,
    recordId,
}) => (
    <BulkDeleteWithConfirmButton
        mutationMode='pessimistic'
        mutationOptions={{
            meta: { resource, recordId },
        }}
    />
);

const FileList: FC<FileListProps> = ({
    resource,
    recordId,
}) => (
    <ListBase
        resource='files'
        queryOptions={{
            meta: { resource, recordId },
        }}
    >
        <Datagrid
            bulkActionButtons={(
                <FileBulkActionButtons resource={resource} recordId={recordId} />
            )}
            rowClick={false}
        >
            <FileField />
        </Datagrid>
    </ListBase>
)

export default FileList;
