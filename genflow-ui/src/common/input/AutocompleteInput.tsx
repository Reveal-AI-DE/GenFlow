// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, ReactNode } from 'react';
import {
    AutocompleteInput as RAAutocompleteInput,
    AutocompleteInputProps as RAAutocompleteInputProps,
    RaRecord,
    useChoicesContext,
} from 'react-admin';

interface AutocompleteInputProps extends Omit<RAAutocompleteInputProps, 'renderInput'> {
    renderStartAdornment?: (record: RaRecord) => ReactNode;
};

const AutocompleteInput: FC<AutocompleteInputProps> = ({
    renderStartAdornment,
    ...rest
}) => {
    const { selectedChoices } = useChoicesContext()

    return (selectedChoices && selectedChoices[0]) ? (
        <RAAutocompleteInput
            TextFieldProps={{
                InputProps: {
                    startAdornment: (renderStartAdornment) ?
                        renderStartAdornment(selectedChoices[0]) : null,
                },
            }}
            {...rest}
        />
    ) : (
        <RAAutocompleteInput
            {...rest}
        />
    );
};

export default AutocompleteInput;
