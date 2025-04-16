// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';

import modelDataProvider from '@/provider/model/modelDataProvider';
import { ModelSelectInput } from '@/provider/model/form';
import { ModelConfigCard } from '@/provider/model/show';

const ModelResourceProps: ResourceProps = {
    name: 'models',
};

export {
    ModelResourceProps,
    ModelSelectInput,
    ModelConfigCard,
    modelDataProvider,
};
