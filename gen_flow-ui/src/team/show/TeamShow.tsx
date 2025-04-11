// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Stack from '@mui/material/Stack';
import {
    TextField, Labeled, FunctionField, DateField, ShowBase,
    TopToolbar, DeleteWithConfirmButton, useRecordContext
} from 'react-admin';

import { Team } from '@/types';
import { UserField } from '@/user';
import { TeamEditButton } from '@/team/form';

type TeamShowProps = object;

const TeamShow: FC<TeamShowProps> = () => {
    const team = useRecordContext<Team>();

    if (!team) {
        return null;
    }

    return (
        <ShowBase
            id={team.id}
        >
            <TopToolbar>
                <DeleteWithConfirmButton
                    confirmTitle='message.delete_dialog.title'
                    confirmContent='message.delete_dialog.content'
                    translateOptions={{ name: team.name, resource: 'team' }}
                />
                <TeamEditButton />
            </TopToolbar>

            <Stack direction='row' spacing={4}>
                <Stack spacing={2}>
                    <Labeled source='name'>
                        <TextField source='name' />
                    </Labeled>
                    <Labeled source='created_date'>
                        <DateField source='created_date' showTime />
                    </Labeled>
                </Stack>

                <Stack spacing={2}>
                    <Labeled source='description'>
                        <TextField source='description' />
                    </Labeled>
                    <Labeled source='created_by'>
                        <FunctionField
                            source='created_by'
                            render={(record) => <UserField user={record.owner} />}
                            sortable={false}
                        />
                    </Labeled>
                </Stack>

            </Stack>
        </ShowBase>
    )
};

export default TeamShow;
