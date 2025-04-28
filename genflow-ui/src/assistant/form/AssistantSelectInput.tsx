// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useCallback } from 'react';
import {
    ReferenceInput,
    ReferenceInputProps,
    AutocompleteInputProps,
    RecordContextProvider,
} from 'react-admin';

import { AutocompleteInput } from '@/common';
import { EntityFieldSlot } from '@/entity';
import { AssistantField } from '@/assistant/show';

interface AssistantSelectInputProps extends Omit<ReferenceInputProps, 'reference'> {
    onChange?: AutocompleteInputProps['onChange'];
};

const AssistantSelectInput: FC<AssistantSelectInputProps> = ({
    source,
    validate,
    label,
    onChange,
    ...rest
}) => {
    const renderStartAdornment = useCallback((record: any) => (
        <RecordContextProvider key={record.id} value={record}>
            <AssistantField
                slots={[EntityFieldSlot.AVATAR]}
            />
        </RecordContextProvider>
    ), []);

    const renderOptionText = useCallback((choice: any) => (
        <RecordContextProvider key={choice.id} value={choice}>
            <AssistantField />
        </RecordContextProvider>
    ), []);

    return (
        <ReferenceInput
            source={source}
            reference='assistants'
            {...rest}
        >
            <AutocompleteInput
                label={label}
                variant='outlined'
                validate={validate}
                debounce={500}
                optionText={renderOptionText}
                inputText={(choice) => choice?.name}
                groupBy={(choice) => choice?.group?.name}
                margin='none'
                onChange={onChange}
                renderStartAdornment={renderStartAdornment}
            />
        </ReferenceInput>
    );
};
export default AssistantSelectInput;
