// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Divider from '@mui/material/Divider';
import {
    FunctionField, SimpleShowLayout, useRecordContext, RecordContextProvider,
} from 'react-admin';

import { ModelConfigWithEntity } from '@/types';
import { ProviderField } from '@/provider/show';
import ModelField from '@/provider/model/show/ModelField';
import ModelParameters from '@/provider/model/show/ModelParameters';

type ModelConfigCardProps = object;

const ModelConfigCard: FC<ModelConfigCardProps> = () => {
    const modelConfigWithEntity = useRecordContext<ModelConfigWithEntity>();

    if (!modelConfigWithEntity) {
        return null;
    }

    return (
        <SimpleShowLayout
            spacing={1}
            sx={{ pl: 0 }}
            divider={<Divider />}
        >
            <FunctionField
                source='related_model.provider_name'
                render={() => (
                    <ProviderField entity={modelConfigWithEntity.entity.provider} />
                )}
            />
            <FunctionField
                source='related_model.model_name'
                render={() => (
                    <RecordContextProvider value={modelConfigWithEntity.entity}>
                        <ModelField />
                    </RecordContextProvider>
                )}
            />
            {
                modelConfigWithEntity.entity.parameter_configs && (
                    <FunctionField
                        source='related_model.config.parameters'
                        render={() => modelConfigWithEntity.entity.parameter_configs && (
                            <ModelParameters
                                namePrefix='related_model.config.parameters'
                                parameterConfigs={modelConfigWithEntity.entity.parameter_configs}
                                parameters={modelConfigWithEntity.config.parameters}
                            />
                        )}
                    />
                )
            }
        </SimpleShowLayout>
    );
}

export default ModelConfigCard;
