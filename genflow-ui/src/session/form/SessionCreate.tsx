// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import AddIcon from '@mui/icons-material/Add';
import Skeleton from '@mui/material/Skeleton';
import { styled } from '@mui/material/styles';
import { useWatch } from 'react-hook-form'
import {
    Form, SelectInput, SaveButton, CreateBase,
    required, AutocompleteInput, Title, useTranslate,
} from 'react-admin';

import {
    SessionType, Session, ModelType,
    PromptStatus, AssistantStatus,
} from '@/types';
import { ModelSelectInput } from '@/provider/model';
import { PromptSelectInput } from '@/prompt';
import { AssistantSelectInput } from '@/assistant';
import { getChoicesFromEnum } from '@/utils';
import { ChatLayout } from '@/layout';
import NewSessionPlaceholder from '@/session/form/NewSessionPlaceholder';

const SelectRelated: FC = () => {
    const { session_type: sessionType } = useWatch<Session>();

    if (!sessionType) {
        return (
            <Skeleton animation='wave'>
                <AutocompleteInput
                    source='related_model.model_name'
                    margin='none'
                />
            </Skeleton>
        );
    }

    if (sessionType === SessionType.LLM) {
        return (
            <ModelSelectInput
                disabled={!sessionType}
                label={false}
                variant='outlined'
                validate={required()}
                filter={{ model_type: ModelType.LLM, enabled_only: true }}
            />
        );
    }

    if (sessionType === SessionType.PROMPT) {
        return (
            <PromptSelectInput
                source='related_prompt'
                label={false}
                disabled={!sessionType}
                validate={required()}
                filter={{ prompt_status: PromptStatus.PUBLISHED }}
                sort={{ field: 'group__name', order: 'ASC' }}
            />
        );
    }

    if (sessionType === SessionType.ASSISTANT) {
        return (
            <AssistantSelectInput
                source='related_assistant'
                label={false}
                disabled={!sessionType}
                validate={required()}
                filter={{ assistant_status: AssistantStatus.PUBLISHED }}
                sort={{ field: 'group__name', order: 'ASC' }}
            />
        );
    }

    return null;
};

const Content = styled(Box, {
    name: 'GFNewChat',
    slot: 'content',
})(() => ({
    height: '100%',
}));

const FormContainer = styled(Box, {
    name: 'GFSessionCreate',
    slot: 'form',
})(({ theme }) => ({
    height: '20%',
    margin: theme.spacing(4),
}));

const ButtonContainer = styled(Grid, {
    name: 'GFSessionCreate',
    slot: 'button',
})(({ theme }) => ({
    [theme.breakpoints.down('sm')]: {
        textAlign: 'center',
    }
}));

const StyledSelectInput = styled(SelectInput)({
    '& legend': {
        width: 0,
    },
    marginTop: 0,
    minWidth: 'auto',
});

type SessionCreateProps = object

const SessionCreate: FC<SessionCreateProps> = () => {
    const translate = useTranslate();

    const transform = ({
        name,
        related_model,
        related_prompt,
        related_assistant,
        ...data
    }: Session): Session => ({
        name: 'New Chat',
        related_model: data.session_type === SessionType.LLM ? related_model : undefined,
        related_prompt: data.session_type === SessionType.PROMPT ? related_prompt : undefined,
        related_assistant: data.session_type === SessionType.ASSISTANT ? related_assistant : undefined,
        ...data,
    });

    return (
        <ChatLayout>
            <Title title={translate('label.new')} />
            <FormContainer>
                <CreateBase
                    redirect='show'
                    resource='sessions'
                    transform={transform}
                >
                    <Form>
                        <Grid
                            container
                            rowSpacing={{
                                xs: 0
                            }}
                            columnSpacing={4}
                        >
                            <Grid
                                size={{
                                    xs: 12,
                                    sm: 12,
                                    md: 2
                                }}
                            >
                                <StyledSelectInput
                                    source='session_type'
                                    label={false}
                                    choices={getChoicesFromEnum(SessionType)}
                                    defaultValue={SessionType.LLM}
                                    validate={required()}
                                    variant='outlined'
                                    margin='none'
                                />
                            </Grid>
                            <Grid
                                size={{
                                    xs: 12,
                                    sm: 12,
                                    md: 5
                                }}
                            >
                                <SelectRelated />
                            </Grid>
                            <ButtonContainer
                                size={{
                                    xs: 12,
                                    sm: 12,
                                    md: 3
                                }}
                            >
                                <SaveButton
                                    label='label.new'
                                    icon={<AddIcon />}
                                />
                            </ButtonContainer>
                        </Grid>
                    </Form>
                </CreateBase>
            </FormContainer>
            <Content>
                <NewSessionPlaceholder />
            </Content>
        </ChatLayout>
    );
};

export default SessionCreate;
