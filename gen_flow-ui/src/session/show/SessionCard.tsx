// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Card from '@mui/material/Card';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Chip from '@mui/material/Chip';
import { styled } from '@mui/material/styles';
import {
    useRecordContext, DateField, useTranslate,
    Labeled, RecordContextProvider, ResourceContextProvider,
} from 'react-admin';

import { Session, SessionType } from '@/types';
import { UserField } from '@/user';
import { ModelConfigCard } from '@/provider/model';
import { PromptInfo } from '@/prompt';
import { SessionName } from '@/session/form';

const StyledStack = styled(Stack, {
    name: 'GFSessionCardHeader',
    slot: 'root',
})(({ theme }) => ({
    margin: theme.spacing(2),
    marginLeft: theme.spacing(0),
}));

type SessionCardHeaderProps = object;

const SessionCardHeader: FC<SessionCardHeaderProps> = () => {
    const session = useRecordContext<Session>();
    const translate = useTranslate();

    if (!session) {
        return null;
    }

    return (
        <StyledStack
            direction='row'
            spacing={2}
            divider={(
                <Divider
                    orientation='vertical'
                    flexItem
                />
            )}
        >
            <Chip
                title={translate('resources.sessions.fields.session_type')}
                label={session.session_type.toUpperCase()}
                color='primary'
                variant='outlined'
                size='small'
            />
            <Labeled source='owner.username'>
                <UserField user={session.owner} />
            </Labeled>
            <Labeled source='created_date'>
                <DateField source='created_date' showTime />
            </Labeled>
        </StyledStack>
    );
};

const StyledCard = styled(Card, {
    name: 'GFSessionCard',
    slot: 'root',
})(() => ({
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
}));

type SessionCardProps = object;

const SessionCard: FC<SessionCardProps> = () => {
    const session = useRecordContext<Session>();

    if (!session) {
        return null;
    }

    return (
        <StyledCard>
            <CardHeader
                title={<SessionName />}
                subheader={(
                    <SessionCardHeader />
                )}
            />
            <CardContent>
                {
                    session.session_type === SessionType.LLM && (
                        <RecordContextProvider value={session.related_model}>
                            <ModelConfigCard />
                        </RecordContextProvider>
                    )
                }
                {
                    session.session_type === SessionType.PROMPT && (
                        <ResourceContextProvider value='prompts'>
                            <RecordContextProvider value={session.related_prompt}>
                                <PromptInfo />
                            </RecordContextProvider>
                        </ResourceContextProvider>
                    )
                }
                <Divider />
            </CardContent>
        </StyledCard>
    );
};

export default SessionCard;
