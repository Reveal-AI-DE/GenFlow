// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { required, TextInput } from 'react-admin';

import { ModelType } from '@/types';
import { ExpandableTextInput, ImageInput } from '@/common';
import { QuestionsInput } from '@/entity';
import { ModelSelectInput } from '@/provider/model';
import { GroupSelectInput } from '@/group';

type PromptSetupFormProps = object

const PromptSetupForm: FC<PromptSetupFormProps> = () => (
    <>
        <ImageInput
            source='avatar'
            sx={{
                flexDirection: 'row',
                '& .RaImageField-image': {
                    width: '100px !important',
                    height: '50px !important',
                },
            }}
        />
        <GroupSelectInput
            source='group.id'
            reference='prompt-groups'
        />
        <TextInput
            source='name'
            variant='outlined'
            validate={required()}
        />
        <TextInput
            source='description'
            variant='outlined'
            validate={required()}
            multiline
            rows={2}
        />
        <ExpandableTextInput
            source='pre_prompt'
            variant='outlined'
            validate={required()}
        />
        <QuestionsInput source='suggested_questions' />
        <ModelSelectInput
            variant='outlined'
            validate={required()}
            filter={{ model_type: ModelType.LLM, enabled_only: true }}
        />
    </>
);

export default PromptSetupForm;
