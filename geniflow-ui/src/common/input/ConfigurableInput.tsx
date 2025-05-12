// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Tooltip from '@mui/material/Tooltip';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import InputAdornment from '@mui/material/InputAdornment';
import {
    SelectInput, BooleanInput,
    required, useLocale, minValue, maxValue,
    TextInput, NumberInput,
} from 'react-admin';

import {
    ConfigurationType, ConfigurationEntity, TranslationEntity,
    NumberConfigurationEntity, StringConfigurationEntity,
} from '@/types';
import SliderInput from '@/common/input/SliderInput';
import TextareaAutosize from '@/common/input/TextareaAutosize';

interface HelpIconProps {
    helpEntity?: TranslationEntity;
    locale: string;
}

const HelpIcon: FC<HelpIconProps> = ({
    locale,
    helpEntity,
}) => (helpEntity ? (
    <Tooltip title={helpEntity[locale] ?? helpEntity.en_US}>
        <InfoOutlinedIcon fontSize='small' />
    </Tooltip>
) : null);

const renderStartAdornment = (configurationEntity: ConfigurationEntity, locale: string): JSX.Element | null => (
    (
        configurationEntity.type === ConfigurationType.STRING &&
        (configurationEntity as StringConfigurationEntity).options
    ) ? (
            <InputAdornment position='start'>
                <HelpIcon locale={locale} helpEntity={configurationEntity.help} />
            </InputAdornment>
        ) : null
);

const renderEndAdornment = (configurationEntity: ConfigurationEntity, locale: string): JSX.Element | null => (
    (
        configurationEntity.type !== ConfigurationType.STRING ||
        (configurationEntity as StringConfigurationEntity).options === undefined
    ) ? (
            <InputAdornment position='end'>
                <HelpIcon locale={locale} helpEntity={configurationEntity.help} />
            </InputAdornment>
        ) : null
);

export interface ConfigurableInputProps {
    configurationEntity: ConfigurationEntity;
    defaultValue?: any;
    onChange?: (value: any, configurationEntity: ConfigurationEntity) => void;
}

const ConfigurableInput: FC<ConfigurableInputProps> = ({
    configurationEntity,
    defaultValue,
    onChange,
}) => {
    const locale = useLocale();

    const defaultParams = (): any => ({
        source: configurationEntity.name,
        label: configurationEntity.label[locale] ?? configurationEntity.label.en_US,
        variant: 'outlined',
        fullWidth: true,
        onChange: onChange ? (e: React.ChangeEvent<HTMLInputElement>) => (
            onChange(e.target.value, configurationEntity)
        ) : undefined,
        InputProps:
        configurationEntity.help ? ({
            startAdornment: renderStartAdornment(configurationEntity, locale),
            endAdornment: renderEndAdornment(configurationEntity, locale),
        }) : undefined,
    });

    const validators: any[] = configurationEntity.required ? [required()] : [];

    switch(configurationEntity.type) {
        case ConfigurationType.FLOAT:
        case ConfigurationType.INT: {
            const numberConfigurationEntity = configurationEntity as NumberConfigurationEntity;
            if (numberConfigurationEntity.min) {
                validators.push(minValue(numberConfigurationEntity.min));
            }
            if (numberConfigurationEntity.max) {
                validators.push(maxValue(numberConfigurationEntity.max));
            }
            const step = numberConfigurationEntity.precision ? 1 / 10**numberConfigurationEntity.precision : 1;

            if (configurationEntity.type === ConfigurationType.INT) {
                return (
                    <NumberInput
                        validate={validators}
                        defaultValue={defaultValue}
                        min={numberConfigurationEntity.min ? numberConfigurationEntity.min : undefined}
                        max={numberConfigurationEntity.max ? numberConfigurationEntity.max : undefined}
                        step={step}
                        {...defaultParams()}

                    />
                );
            }

            return (
                <SliderInput
                    validate={validators}
                    defaultValue={defaultValue}
                    min={numberConfigurationEntity.min}
                    max={numberConfigurationEntity.max}
                    step={step}
                    margin='dense'
                    {...defaultParams()}
                />
            );
        }
        case ConfigurationType.BOOLEAN: {
            return (
                <BooleanInput
                    validate={validators}
                    options={{
                        checkedIcon: <CheckCircleIcon />,
                    }}
                    defaultValue={defaultValue}
                    {...defaultParams()}
                />
            );
        }
        case ConfigurationType.SECRET:
        case ConfigurationType.STRING: {
            const stringConfigurationEntity = configurationEntity as StringConfigurationEntity;
            if (stringConfigurationEntity.options && stringConfigurationEntity.options.length > 0) {
                const { onChange: providedOnChange, ...rest } = defaultParams();
                return (
                    <SelectInput
                        choices={
                            stringConfigurationEntity.options.map(
                                (item: ConfigurationEntity) => ({
                                    id: item.name,
                                    name: item.label[locale] ?? item.label.en_US,
                                    disabled: item.disabled,
                                }),
                            )
                        }
                        defaultValue={defaultValue}
                        validate={validators}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                            if (providedOnChange) {
                                providedOnChange(e.target.value, configurationEntity);
                            }
                        }}
                        {...rest}
                    />
                );
            }
            return (
                <TextInput
                    defaultValue={defaultValue}
                    validate={validators}
                    {...defaultParams()}
                    inputProps={{
                        type: stringConfigurationEntity.type === ConfigurationType.SECRET ? 'password' : 'text',
                    }}
                />
            );
        }
        case ConfigurationType.TEXT: {
            return (
                <TextareaAutosize
                    formControlProps={{}}
                    inputProps={{
                        minRows: 1,
                        maxRows: 4,
                        onChange: ((e) => {
                            if (onChange) {
                                onChange(e.target.value, configurationEntity);
                            }
                        })
                    }}
                />
            );
        }
        case ConfigurationType.OBJECT: {
            return null;
        }
        default:
            return null;
    }
};

export default ConfigurableInput;
