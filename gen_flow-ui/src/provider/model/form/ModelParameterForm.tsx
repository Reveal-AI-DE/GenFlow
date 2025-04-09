// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useEffect, useState } from 'react';
import {
    useDataProvider, Labeled,
} from 'react-admin';
import { useWatch } from 'react-hook-form';

import { ConfigurationEntity } from '@/types';
import { ConfigurableInputForm } from '@/common';

interface ModelParameterFormProps {
    modelInputName?: string;
    source?: string;
};

const ModelParameterForm: FC<ModelParameterFormProps> = ({
    modelInputName = 'related_model.model_name',
    source = 'related_model.config.parameters',
}) => {
    const modelName = useWatch({ name: modelInputName });
    if (!modelName) {
        return null;
    }

    const [configs, setConfigs] = useState<ConfigurationEntity[]>([]);
    const dataProvider = useDataProvider();

    useEffect(() => {
        const fetchConfigurations = async (): Promise<void> => {
            const convertedConfigurations = await dataProvider.getParameterConfig('models', {
                id: modelName,
            }).then((parametersData: any) => {
                const { data: parameterConfig } = parametersData;
                return parameterConfig.map((config: ConfigurationEntity) => {
                    const inputName = `${source}.${config.name}`;
                    return {
                        ...config,
                        name: inputName,
                    };
                });
            });
            setConfigs(convertedConfigurations);
        }
        if (modelName) {
            fetchConfigurations();
        }
    }, [modelName]);

    if (configs.length === 0) {
        return null;
    }

    return (
        <Labeled source='related_model.config.parameters'>
            <ConfigurableInputForm
                parameterConfigs={configs}
            />
        </Labeled>
    );
};

export default ModelParameterForm;
