// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
