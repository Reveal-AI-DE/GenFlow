// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    required, TextInput,
    ArrayInput, SimpleFormIterator,
} from 'react-admin';

import { ModelType } from '@/types';
import { ExpandableTextInput, ImageInput } from '@/common';
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
        <ArrayInput
            source='suggested_questions'
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
        <ModelSelectInput
            variant='outlined'
            validate={required()}
            filter={{ model_type: ModelType.LLM, enabled_only: true }}
        />
    </>
);

export default PromptSetupForm;
