// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    useRecordContext, SimpleShowLayout,
    TextField, ReferenceField, RecordContextProvider,
} from 'react-admin';

import { Prompt } from '@/types';
import { TruncatedTextField } from '@/common';
import { ModelConfigCard } from '@/provider/model';
import { GroupField } from '@/group';

type PromptInfoProps = object;

const PromptInfo: FC<PromptInfoProps> = () => {
    const record = useRecordContext<Prompt>();

    if (!record) {
        return null;
    }

    return (
        <>
            <SimpleShowLayout
                spacing={1}
                sx={{ pl: 0 }}
            >
                <ReferenceField
                    source='group_id'
                    reference='prompt-groups'
                >
                    <GroupField />
                </ReferenceField>
                <TextField source='name' />
                <TruncatedTextField source='description' />
                <TruncatedTextField source='pre_prompt' />
            </SimpleShowLayout>
            <RecordContextProvider value={record.related_model}>
                <ModelConfigCard />
            </RecordContextProvider>
        </>

    );
};

export default PromptInfo;
