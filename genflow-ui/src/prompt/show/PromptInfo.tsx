// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import {
    useRecordContext, RecordContextProvider,
} from 'react-admin';

import { Prompt } from '@/types';
import { TruncatedTextField } from '@/common';
import { EntityInfo } from '@/entity';
import { ModelConfigCard } from '@/provider/model';

type PromptInfoProps = object;

const PromptInfo: FC<PromptInfoProps> = () => {
    const prompt = useRecordContext<Prompt>();

    if (!prompt) {
        return null;
    }

    return (
        <EntityInfo
            additionalFields={(
                <TruncatedTextField source='pre_prompt' />
            )}
        >
            <RecordContextProvider value={prompt.related_model}>
                <ModelConfigCard />
            </RecordContextProvider>
        </EntityInfo>

    );
};

export default PromptInfo;
