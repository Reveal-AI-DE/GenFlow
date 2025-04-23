// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    useRecordContext, SimpleShowLayout, FunctionField,
    TextField, RecordContextProvider,
} from 'react-admin';

import { Prompt } from '@/types';
import { TruncatedTextField } from '@/common';
import { ModelConfigCard } from '@/provider/model';
import { GroupField } from '@/group';

type PromptInfoProps = object;

const PromptInfo: FC<PromptInfoProps> = () => {
    const prompt = useRecordContext<Prompt>();

    if (!prompt) {
        return null;
    }

    return (
        <>
            <SimpleShowLayout
                spacing={1}
                sx={{ pl: 0 }}
            >
                <FunctionField
                    source='group.id'
                    render={(record) => (
                        <RecordContextProvider value={record.group}>
                            <GroupField />
                        </RecordContextProvider>
                    )}
                />
                <TextField source='name' />
                <TruncatedTextField source='description' />
                <TruncatedTextField source='pre_prompt' />
            </SimpleShowLayout>
            <RecordContextProvider value={prompt.related_model}>
                <ModelConfigCard />
            </RecordContextProvider>
        </>

    );
};

export default PromptInfo;
