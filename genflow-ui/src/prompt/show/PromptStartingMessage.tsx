// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    RecordContextProvider, useRecordContext
} from 'react-admin';

import { Session } from '@/types';
import { EntityStartingMessage } from '@/entity';

type PromptStartingMessageProps = object;

const PromptStartingMessage: FC<PromptStartingMessageProps> = () => {
    const session = useRecordContext<Session>();

    if (!session || !session.related_prompt) {
        return null;
    }

    const prompt = session.related_prompt;

    return (
        <RecordContextProvider value={prompt}>
            <EntityStartingMessage />
        </RecordContextProvider>
    );
};

export default PromptStartingMessage;
