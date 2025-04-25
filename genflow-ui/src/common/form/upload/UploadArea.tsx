// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Uploady, { UploadyProps } from '@rpldy/uploady';

import DropZone, { DropZoneProps } from './DropZone';

import UploadList from '@/common/form/upload/UploadList';

interface UploadAreaProps extends UploadyProps {
    dropZoneOptions: DropZoneProps,
}

const UploadArea: FC<UploadAreaProps> = ({
    dropZoneOptions,
    ...rest
}) => (
    <Uploady
        {...rest}
    >
        <Box>
            <DropZone
                {...dropZoneOptions}
            />
            <UploadList />
        </Box>
    </Uploady>
);

export default UploadArea;
