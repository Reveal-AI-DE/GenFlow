// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Grid from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import { useTranslate } from 'react-admin';

import { ConfigurationEntity } from '@/types';
import {
    ControlledAccordion, ConfigurableInput,
    ConfigurableInputProps,
} from '@/common';

interface ConfigurableInputFormProps {
    parameterConfigs: ConfigurationEntity[],
    onChange?: ConfigurableInputProps['onChange'],
};

const ConfigurableInputForm: FC<ConfigurableInputFormProps> = ({
    parameterConfigs,
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
            defaultValue={config.default}
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
