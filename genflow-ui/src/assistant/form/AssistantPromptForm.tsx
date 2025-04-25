// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    required, TextInput,
    AutocompleteInputProps,
} from 'react-admin';
import { useFormContext } from 'react-hook-form'

import { PromptStatus, ModelType } from '@/types';
import { PromptSelectInput } from '@/prompt/form';
import { ExpandableTextInput, ImageInput } from '@/common';
import { ModelSelectInput, ModelParameterForm } from '@/provider/model';
import { GroupSelectInput } from '@/group';

type AssistantPromptFormFormProps = object;

const AssistantPromptForm: FC<AssistantPromptFormFormProps> = () => {
    const { setValue } = useFormContext();
    const onPromptTemplateChange: AutocompleteInputProps['onChange'] = (
        value,
        record
    ) => {
        if (!record) {
            return;
        }
        setValue('pre_prompt', record.pre_prompt);
        setValue('related_model', record.related_model);
    };

    return (
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
                reference='assistant-groups'
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
            <PromptSelectInput
                source='use_prompt_template'
                filter={{ status: PromptStatus.PUBLISHED }}
                sort={{ field: 'group__name', order: 'ASC' }}
                onChange={onPromptTemplateChange}
            />
            <ExpandableTextInput
                source='pre_prompt'
                variant='outlined'
                validate={required()}
            />
            <ModelSelectInput
                variant='outlined'
                validate={required()}
                filter={{ model_type: ModelType.LLM, enabled_only: true }}
            />
            <ModelParameterForm />
        </>
    );
}

export default AssistantPromptForm;
