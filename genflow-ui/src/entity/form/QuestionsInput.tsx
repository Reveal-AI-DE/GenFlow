// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    required, TextInput,
    ArrayInput, SimpleFormIterator,
} from 'react-admin';

interface QuestionsInputProps {
    source?: string;
};

const QuestionsInput: FC<QuestionsInputProps> = ({
    source = 'suggested_questions',
}) => (
    <ArrayInput
        source={source}
    >
        <SimpleFormIterator
            inline
        >
            <TextInput
                source='question'
                variant='outlined'
                validate={required()}
            />
        </SimpleFormIterator>
    </ArrayInput>
);

export default QuestionsInput;
