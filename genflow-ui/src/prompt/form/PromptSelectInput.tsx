// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useCallback } from 'react';
import {
    ReferenceInput,
    ReferenceInputProps,
    AutocompleteInputProps,
    RecordContextProvider,
} from 'react-admin';

import { AutocompleteInput, EntityFieldSlot } from '@/common';
import { PromptField } from '@/prompt/show';

interface PromptSelectInputProps extends Omit<ReferenceInputProps, 'reference'> {
    onChange?: AutocompleteInputProps['onChange'];
};

const PromptSelectInput: FC<PromptSelectInputProps> = ({
    source,
    validate,
    label,
    onChange,
    ...rest
}) => {
    const renderStartAdornment = useCallback((record: any) => (
        <RecordContextProvider key={record.id} value={record}>
            <PromptField
                slots={[EntityFieldSlot.AVATAR]}
            />
        </RecordContextProvider>
    ), []);

    const renderOptionText = useCallback((choice: any) => (
        <RecordContextProvider key={choice.id} value={choice}>
            <PromptField />
        </RecordContextProvider>
    ), []);

    return (
        <ReferenceInput
            source={source}
            reference='prompts'
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
export default PromptSelectInput;
