// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import { useRecordContext } from 'react-admin';

import { FileEntity } from '@/types';
import { truncateText } from '@/utils';

type FileFieldProps = object;

const FileField: FC<FileFieldProps> = () => {
    const fileEntity = useRecordContext<FileEntity>();

    if (!fileEntity) {
        return null;
    }

    return (
        <span>{truncateText(fileEntity.id as string, 50, 'characters')}</span>
    );
};

export default FileField;
