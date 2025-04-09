// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';

import modelDataProvider from '@/provider/model/modelDataProvider';

const ModelResourceProps: ResourceProps = {
    name: 'models',
};

export {
    ModelResourceProps,
    modelDataProvider,
};
