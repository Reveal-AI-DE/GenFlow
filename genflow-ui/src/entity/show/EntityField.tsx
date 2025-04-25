// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, Fragment } from 'react';
import Tooltip from '@mui/material/Tooltip';
import Stack from '@mui/material/Stack';
import Avatar from '@mui/material/Avatar';
import { useRecordContext } from 'react-admin';

import { CommonEntity } from '@/types';

export enum EntityFieldSlot {
    AVATAR = 'avatar',
    NAME = 'name',
}

export interface EntityFieldProps {
    slots?: EntityFieldSlot[];
};

const EntityField: FC<EntityFieldProps> = ({
    slots=[EntityFieldSlot.AVATAR, EntityFieldSlot.NAME],
}) => {
    const record = useRecordContext<CommonEntity>();
    if (!record) {
        return null;
    }

    const renderSlot = (slot: EntityFieldSlot): JSX.Element | null => {
        switch (slot) {
            case EntityFieldSlot.AVATAR:
                return (
                    <Avatar
                        src={record.avatar}
                        alt={record.name}
                        sx={{ width: 30, height: 30 }}
                    >
                        {!record.avatar && record.name[0]}
                    </Avatar>
                );
            case EntityFieldSlot.NAME:
                return (
                    <span>{record.name}</span>
                );
            default:
                return null;
        }
    };

    return (
        <Tooltip title={record.description}>
            <Stack
                direction='row'
                spacing={1}
                alignItems='center'
            >
                {
                    slots.map((slot: EntityFieldSlot) => (
                        <Fragment key={slot}>
                            {renderSlot(slot)}
                        </Fragment>
                    ))
                }
            </Stack>
        </Tooltip>
    );
};

export default EntityField;
