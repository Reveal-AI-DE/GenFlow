// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import IconButton from '@mui/material/IconButton';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { styled } from '@mui/material/styles';
import {
    RecordContextProvider, useRecordContext
} from 'react-admin';

import { Session } from '@/types';
import { useChatHandler } from '@/hook';
import { PagePlaceholder } from '@/common';
import PromptField from '@/prompt/show/PromptField';

const Root = styled(Box, {
    name: 'GFPromptStartingMessage',
    slot: 'root',
})(({ theme }) => ({
    maxWidth: '600px',
    margin: theme.spacing(2),
}));

const DescriptionContainer = styled(Typography, {
    name: 'GFPromptStartingMessage',
    slot: 'description',
})(({ theme }) => ({
    padding: theme.spacing(1),
}));

const QuestionContainer = styled(Typography, {
    name: 'GFPromptStartingMessage',
    slot: 'question',
})(({ theme }) => ({
    paddingLeft: theme.spacing(1),
    paddingRight: theme.spacing(1),
    textAlign: 'left'
}));

type PromptStartingMessageProps = object;

const PromptStartingMessage: FC<PromptStartingMessageProps> = () => {
    const session = useRecordContext<Session>();
    const { handleSendMessage } = useChatHandler();

    if (!session || !session.related_prompt) {
        return null;
    }

    const prompt = session.related_prompt;

    return (
        <PagePlaceholder>
            <Root>
                <RecordContextProvider value={prompt}>
                    <PromptField />
                </RecordContextProvider>
                <DescriptionContainer
                    variant='subtitle1'
                    variantMapping={{ subtitle1: 'p' }}
                    gutterBottom
                >
                    {prompt.description}
                </DescriptionContainer>
                {
                    prompt.suggested_questions && prompt.suggested_questions.map((question, index) => (
                        <IconButton
                            key={index}
                            onClick={() => handleSendMessage(question.question)}
                        >
                            <Paper
                                elevation={2}
                            >
                                <QuestionContainer
                                    variant='subtitle1'
                                    variantMapping={{ subtitle1: 'p' }}
                                    gutterBottom
                                >
                                    {question.question}
                                </QuestionContainer>
                            </Paper>
                        </IconButton>
                    ))
                }
            </Root>
        </PagePlaceholder>
    );
};

export default PromptStartingMessage;
