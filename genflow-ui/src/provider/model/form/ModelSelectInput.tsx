// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useCallback } from 'react';
import {
    ReferenceInput, TextInput,
    AutocompleteInputProps, ReferenceInputProps,
    useLocale, RecordContextProvider, RaRecord,
} from 'react-admin';
import { useFormContext } from 'react-hook-form'

import { ModelWithProviderEntity } from '@/types';
import { AutocompleteInput } from '@/common';
import { ModelField, ModelFieldSlot } from '@/provider/model/show';

interface ModelSelectInputProps extends Omit<AutocompleteInputProps, 'source' | 'filter' | 'disabled'> {
    filter: ReferenceInputProps['filter'];
    disabled?: boolean;
    onChange?: AutocompleteInputProps['onChange'];
    source?: string;
};

const ModelSelectInput: FC<ModelSelectInputProps> = ({
    filter,
    disabled,
    onChange,
    source = 'related_model',
    ...rest
}) => {
    const { setValue } = useFormContext();
    const locale = useLocale();

    const renderOptionText = useCallback((choice: RaRecord) => (
        <RecordContextProvider key={choice.id} value={choice}>
            <ModelField
                slots={[ModelFieldSlot.NAME, ModelFieldSlot.PROPERTIES]}
            />
        </RecordContextProvider>
    ), []);

    const renderStartAdornment = useCallback((record: RaRecord) => (
        <RecordContextProvider key={record.id} value={record}>
            <ModelField
                slots={[ModelFieldSlot.PROPERTIES]}
            />
        </RecordContextProvider>
    ), []);

    const handleModelChange: AutocompleteInputProps['onChange'] = (
        value,
        record
    ) => {
        if (!record) {
            return;
        }
        setValue(`${source}.model_name`, (record as ModelWithProviderEntity).id);
        setValue(`${source}.provider_name`, (record as ModelWithProviderEntity).provider.id);
        if (onChange) {
            onChange(value, record);
        }
    };

    return (
        <>
            <ReferenceInput
                source={`${source}.model_name`}
                reference='models'
                filter={filter}
                perPage={-1}
                disabled={disabled}
            >
                <AutocompleteInput
                    debounce={500}
                    optionText={renderOptionText}
                    inputText={(choice) => choice?.label[locale]}
                    margin='none'
                    groupBy={(choice) => choice?.provider.label[locale]}
                    onChange={handleModelChange}
                    renderStartAdornment={renderStartAdornment}
                    {...rest}
                />
            </ReferenceInput>
            <TextInput
                type='hidden'
                source={`${source}.provider_name`}
                sx={{ display: 'none' }}
            />
        </>
    );
};

export default ModelSelectInput;
