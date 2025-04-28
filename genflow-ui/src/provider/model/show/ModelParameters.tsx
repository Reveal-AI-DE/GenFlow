// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Grid from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import { Labeled, TextField, useLocale } from 'react-admin';

import { ConfigurationEntity, Parameters } from '@/types';

type ModelParametersProps = {
    parameterConfigs: ConfigurationEntity[];
    parameters: Parameters;
    namePrefix?: string;
};

const ModelParameters: FC<ModelParametersProps> = ({
    parameterConfigs,
    parameters,
    namePrefix,
}) => {
    const locale = useLocale();
    const configs = parameterConfigs
        .filter((config) => !config.advanced);
    const advancedConfigs = parameterConfigs
        .filter((config) => config.advanced);

    const renderParameter = (config: ConfigurationEntity): JSX.Element => {
        const source = namePrefix ? `${namePrefix}.${config.name}` : ''

        return (
            <Labeled
                source={source}
                label={config.label[locale] ?? config.label.en_US}
            >
                <TextField
                    source={source}
                    defaultValue={
                        parameters[config.name] ? parameters[config.name] as string : config.default as string
                    }
                />
            </Labeled>
        )
    };

    const renderParameters = (configurationEntities: ConfigurationEntity[]): JSX.Element[] => (
        configurationEntities.map(
            (config: ConfigurationEntity, index: React.Key | null | undefined) => (
                <Grid
                    key={index}
                    size={{
                        xs: 12,
                        sm: config.type === 'text' ? 12 : 6
                    }}
                >
                    {renderParameter(config)}
                </Grid>
            ))
    );

    return (
        <Stack
            spacing={1}
        >
            <Grid
                container
                spacing={1}
            >
                {
                    renderParameters(configs)
                }
                {
                    renderParameters(advancedConfigs)
                }
            </Grid>
        </Stack>
    );
}

export default ModelParameters;
