// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
                        render={(record: ModelConfigWithEntity) => record.entity.parameter_configs && (
                            <ModelParameters
                                namePrefix='related_model.config.parameters'
                                parameterConfigs={record.entity.parameter_configs}
                                parameters={record.config.parameters}
                            />
                        )}
                    />
                )
            }
        </SimpleShowLayout>
    );
}

export default ModelConfigCard;
