// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useContext } from 'react';
import IconButton from '@mui/material/IconButton';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { styled } from '@mui/material/styles';
import {
    RecordContextProvider, useRecordContext,
} from 'react-admin';
import get from 'lodash/get';

import { CommonPrompt } from '@/types';
import { SessionContext, SessionContextInterface } from '@/context';
import { PagePlaceholder } from '@/common';
import PromptField from '@/prompt/show/PromptField';

const Root = styled(Box, {
    name: 'GFEntityStartingMessage',
    slot: 'root',
})(({ theme }) => ({
    maxWidth: '600px',
    margin: theme.spacing(2),
}));

const DescriptionContainer = styled(Typography, {
    name: 'GFEntityStartingMessage',
    slot: 'description',
})(({ theme }) => ({
    padding: theme.spacing(1),
}));

const QuestionContainer = styled(Typography, {
    name: 'GFEntityStartingMessage',
    slot: 'question',
})(({ theme }) => ({
    paddingLeft: theme.spacing(1),
    paddingRight: theme.spacing(1),
    textAlign: 'left'
}));

interface EntityStartingMessageProps {
    openingStatementSource?: string;
};

const EntityStartingMessage: FC<EntityStartingMessageProps> = ({
    openingStatementSource='description',
}) => {
    const entity = useRecordContext<CommonPrompt>();

    const {
        setUserInput,
    } = useContext<SessionContextInterface>(SessionContext);
    const onQuestionClicked = (question: string): void => {
        setUserInput(question);
    };

    if (!entity) {
        return null;
    }

    const openingStatement = get(entity, openingStatementSource);

    return (
        <PagePlaceholder>
            <Root>
                <RecordContextProvider value={entity}>
                    <PromptField />
                </RecordContextProvider>
                <DescriptionContainer
                    variant='subtitle1'
                    variantMapping={{ subtitle1: 'p' }}
                    gutterBottom
                >
                    {openingStatement}
                </DescriptionContainer>
                {
                    entity.suggested_questions && entity.suggested_questions.map((question, index) => (
                        <IconButton
                            key={index}
                            onClick={() => onQuestionClicked(question.question)}
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

export default EntityStartingMessage;
