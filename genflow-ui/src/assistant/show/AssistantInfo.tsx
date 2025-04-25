// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    useRecordContext, RecordContextProvider,
} from 'react-admin';

import { Assistant } from '@/types';
import { TruncatedTextField } from '@/common';
import { EntityInfo } from '@/entity';
import { ModelConfigCard } from '@/provider/model';

type AssistantInfoProps = object;

const AssistantInfo: FC<AssistantInfoProps> = () => {
    const assistant = useRecordContext<Assistant>();

    if (!assistant) {
        return null;
    }

    return (
        <EntityInfo
            additionalFields={(
                <TruncatedTextField source='pre_prompt' />
            )}
        >
            <RecordContextProvider value={assistant.related_model}>
                <ModelConfigCard />
            </RecordContextProvider>
        </EntityInfo>

    );
};

export default AssistantInfo;
