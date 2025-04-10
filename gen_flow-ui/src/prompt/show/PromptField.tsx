// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, Fragment } from 'react';
import Tooltip from '@mui/material/Tooltip';
import Stack from '@mui/material/Stack';
import Avatar from '@mui/material/Avatar';
import { useRecordContext } from 'react-admin';

import { Prompt } from '@/types';

export enum PromptFieldSlot {
    AVATAR = 'avatar',
    NAME = 'name',
}

interface PromptFieldProps {
    slots?: PromptFieldSlot[];
};

const PromptField: FC<PromptFieldProps> = ({
    slots=[PromptFieldSlot.AVATAR, PromptFieldSlot.NAME],
}) => {
    const record = useRecordContext<Prompt>();
    if (!record) {
        return null;
    }

    const renderSlot = (slot: PromptFieldSlot): JSX.Element | null => {
        switch (slot) {
            case PromptFieldSlot.AVATAR:
                return (
                    <Avatar
                        src={record.avatar}
                        alt={record.name}
                        sx={{ width: 30, height: 30 }}
                    >
                        {!record.avatar && record.name[0]}
                    </Avatar>
                );
            case PromptFieldSlot.NAME:
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
                    slots.map((slot: PromptFieldSlot) => (
                        <Fragment key={slot}>
                            {renderSlot(slot)}
                        </Fragment>
                    ))
                }
            </Stack>
        </Tooltip>
    );
};

export default PromptField;
