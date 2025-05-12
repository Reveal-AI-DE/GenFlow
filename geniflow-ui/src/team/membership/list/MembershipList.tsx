// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Typography from '@mui/material/Typography';
import {
    ListBase, Datagrid, TextField, FunctionField,
    useTranslate, DeleteWithConfirmButton, ReferenceField,
    useRecordContext, TopToolbar,
} from 'react-admin';

import { Membership, Team, TeamRole } from '@/types';
import { UserField } from '@/user';
import { InvitationCreateButton } from '@/team/invitation';
import { MembershipEditButton } from '@/team/membership/form';

type MembershipListProps = object;

const MembershipList: FC<MembershipListProps> = () => {
    const translate = useTranslate();
    const team = useRecordContext<Team>();

    if (!team) {
        return null;
    }

    return (
        <ListBase
            resource='memberships'
            filter={team ? { team: team.id }: {}}
            sort={{ field: 'joined_date', order: 'DESC' }}
        >
            <TopToolbar>
                <InvitationCreateButton />
            </TopToolbar>
            <Datagrid
                bulkActionButtons={false}
            >
                <FunctionField
                    source='user'
                    render={(record: Membership) => <UserField user={record.user} />}
                    sortable={false}
                />
                <TextField source='role' sortable={false} />
                <FunctionField
                    source='status.label'
                    render={
                        (record: any) => (
                            <>
                                {
                                    record.invitation && (
                                        <ReferenceField source='invitation' reference='invitations'>
                                            <FunctionField
                                                render={
                                                    (invitation: any) => (
                                                        <Typography variant='caption' component='div'>
                                                            {translate(
                                                                'resources.memberships.fields.status.invited',
                                                                {
                                                                    when: invitation.sent_date ?
                                                                        new Date(invitation.sent_date)
                                                                            .toLocaleString() :
                                                                        new Date(invitation.created_date)
                                                                            .toLocaleString(),
                                                                    by: invitation.owner.username,
                                                                }
                                                            )}
                                                        </Typography>
                                                    )
                                                }
                                            />
                                        </ReferenceField>
                                    )
                                }
                                {
                                    record.is_active && record.joined_date && (
                                        <Typography variant='caption' component='div'>
                                            {translate(
                                                'resources.memberships.fields.status.joined',
                                                {
                                                    when: new Date(record.joined_date).toLocaleString()
                                                }
                                            )}
                                        </Typography>
                                    )
                                }
                                {
                                    !record.is_active && record.joined_date && (
                                        <Typography variant='caption' component='div'>
                                            {translate('resources.memberships.fields.status.not_active')}
                                        </Typography>
                                    )
                                }
                            </>
                        )
                    }
                />
                <FunctionField
                    source=''
                    render={
                        (record: any) => (
                            <>
                                {
                                    record.role !== TeamRole.OWNER && (
                                        <DeleteWithConfirmButton
                                            label=''
                                            size='small'
                                            sx={{ minWidth: 'auto' }}
                                            redirect={false}
                                        />
                                    )
                                }
                                {
                                    record.role !== TeamRole.OWNER && (
                                        <MembershipEditButton />
                                    )
                                }
                            </>
                        )
                    }
                />
            </Datagrid>
        </ListBase>
    )
};

export default MembershipList;
