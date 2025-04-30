// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Card from '@mui/material/Card';
import CardHeader, { CardHeaderProps } from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Avatar from '@mui/material/Avatar';
import Chip from '@mui/material/Chip';
import Badge from '@mui/material/Badge';
import { useGetIdentity, DateField, SimpleShowLayout } from 'react-admin';

import { UploadAvatarButton } from '@/user/form/button';

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

    return (
        <Card>
            <CardHeader
                avatar={(
                    <Badge
                        overlap='rectangular'
                        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                        badgeContent={(
                            <UploadAvatarButton />
                        )}
                    >
                        <Avatar
                            src={currentUser.avatar ? currentUser.avatar : undefined}
                            alt={currentUser.fullName || currentUser.email}
                            sx={{
                                width: 128,
                                height: 128
                            }}
                        />
                    </Badge>
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
