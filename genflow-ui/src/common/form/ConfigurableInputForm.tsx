// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Grid from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import { useTranslate } from 'react-admin';

import { ConfigurationEntity, Parameters } from '@/types';
import {
    ControlledAccordion, ConfigurableInput,
    ConfigurableInputProps,
} from '@/common';

interface ConfigurableInputFormProps {
    parameterConfigs: ConfigurationEntity[],
    parameters?: Parameters,
    onChange?: ConfigurableInputProps['onChange'],
};

const ConfigurableInputForm: FC<ConfigurableInputFormProps> = ({
    parameterConfigs,
    parameters,
    onChange,
}) => {
    if (!parameterConfigs || parameterConfigs.length === 0) {
        return null;
    }

    const translate = useTranslate();
    const configs = parameterConfigs.filter(
        (parameterConfig) => !parameterConfig.advanced
    );
    const advancedConfigs = parameterConfigs.filter(
        (parameterConfig) => parameterConfig.advanced
    );

    const renderParameter = (config: ConfigurationEntity): JSX.Element => (
        <ConfigurableInput
            configurationEntity={config}
            defaultValue={parameters ? parameters[config.name]:config.default}
            onChange={onChange}
        />
    )

    const renderParameters = (configurationEntities: ConfigurationEntity[]): JSX.Element => (
        <Stack
            spacing={1}
        >
            <Grid container spacing={1}>
                {
                    configurationEntities.map(
                        (config: ConfigurationEntity, index: React.Key | null | undefined) => (
                            <Grid
                                key={index}
                                size={{
                                    xs: 12,
                                    xl: 6,
                                }}
                            >
                                {renderParameter(config)}
                            </Grid>
                        ))
                }
            </Grid>
        </Stack>
    );

    return (
        <>
            {
                configs.length > 0 && (
                    renderParameters(configs)
                )
            }
            {
                advancedConfigs.length > 0 && (
                    <ControlledAccordion
                        titles={[translate('label.advanced')]}
                    >
                        {renderParameters(advancedConfigs)}
                    </ControlledAccordion>
                )
            }
        </>
    );
};

export default ConfigurableInputForm;
