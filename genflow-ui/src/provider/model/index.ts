// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { ResourceProps } from 'react-admin';

import modelDataProvider from '@/provider/model/modelDataProvider';
import { ModelParameterForm, ModelSelectInput } from '@/provider/model/form';
import { ModelConfigCard } from '@/provider/model/show';

const ModelResourceProps: ResourceProps = {
    name: 'models',
};

export {
    ModelResourceProps,
    ModelParameterForm,
    ModelSelectInput,
    ModelConfigCard,
    modelDataProvider,
};
