// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';

import { FileList } from '@/file/list';
import fileDataProvider from '@/file/fileDataProvider';

const FileResourceProps: ResourceProps = {
    name: 'files',
};

export {
    FileResourceProps,
    FileList,
    fileDataProvider,
};
