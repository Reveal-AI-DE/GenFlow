// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
