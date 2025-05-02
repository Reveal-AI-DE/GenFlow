// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import {
    RecordContextProvider, useRecordContext
} from 'react-admin';

import { Session } from '@/types';
import { EntityStartingMessage } from '@/entity';

type AssistantStartingMessageProps = object;

const AssistantStartingMessage: FC<AssistantStartingMessageProps> = () => {
    const session = useRecordContext<Session>();

    if (!session || !session.related_assistant) {
        return null;
    }

    const prompt = session.related_assistant;

    return (
        <RecordContextProvider value={prompt}>
            <EntityStartingMessage
                openingStatementSource='opening_statement'
            />
        </RecordContextProvider>
    );
};

export default AssistantStartingMessage;
