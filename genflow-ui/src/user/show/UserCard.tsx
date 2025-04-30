// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Card from '@mui/material/Card';
import CardHeader, { CardHeaderProps } from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Avatar from '@mui/material/Avatar';
import Chip from '@mui/material/Chip';
import { useGetIdentity, DateField, SimpleShowLayout } from 'react-admin';

interface UserCardProps {
    actions?: CardHeaderProps['action'];
};

const UserCard: FC<UserCardProps> = ({
    actions,
}) => {
    const { data: currentUser } = useGetIdentity();
    if (!currentUser) {
        return null;
    }

    let avatar = currentUser.avatar ? currentUser.avatar : undefined;
    if (!avatar) {
        if (currentUser.fullName && currentUser.fullName !== '') {
            avatar = currentUser.fullName[0].toUpperCase();
        } else {
            avatar = currentUser.email[0].toUpperCase();
        }
    }

    return (
        <Card>
            <CardHeader
                avatar={(
                    <Avatar
                        src={currentUser.avatar ? currentUser.avatar : undefined}
                    >
                        {avatar}
                    </Avatar>
                )}
                title={(
                    <>
                        <span>
                            {currentUser.fullName}
                        </span>
                        <Chip
                            label={currentUser.username}
                            size='small'
                            variant='filled'
                            sx={{ marginLeft: '8px' }}
                        />
                    </>
                )}
                subheader={currentUser.email}
                action={actions}
            />
            <CardContent>
                <SimpleShowLayout
                    record={currentUser}
                    direction='row'
                >
                    <DateField source='date_joined' showTime />
                    <DateField source='last_login' showTime />
                </SimpleShowLayout>
            </CardContent>
        </Card>
    );
};

export default UserCard;
