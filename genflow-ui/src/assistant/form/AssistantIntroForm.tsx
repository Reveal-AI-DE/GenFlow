// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import { required, TextInput } from 'react-admin';

import { QuestionsInput } from '@/entity';

type AssistantIntroFormProps = object;

const AssistantIntroForm: FC<AssistantIntroFormProps> = () => (
    <>
        <TextInput
            source='opening_statement'
            variant='outlined'
            validate={required()}
            multiline
            rows={4}
        />
        <QuestionsInput
            source='suggested_questions'
        />
    </>
)

export default AssistantIntroForm;
