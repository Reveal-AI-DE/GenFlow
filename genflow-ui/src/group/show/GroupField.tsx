// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, Fragment } from 'react';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useRecordContext } from 'react-admin';
import { styled } from '@mui/material/styles';
import Tooltip from '@mui/material/Tooltip';

import { EntityGroup } from '@/types';

interface StyledBoxProps {
    color: string;
};

const StyledBox = styled(Box, {
    name: 'GFGroupField',
    slot: 'box',
})<{ ownerState: StyledBoxProps }>(({ ownerState }) => ({
    width: 24,
    height: 24,
    border: '1px solid #000',
    backgroundColor: ownerState.color,
}));

export enum GroupFieldSlot {
    COLOR = 'box',
    LABEL = 'label',
}

interface GroupFieldProps {
    slots?: GroupFieldSlot[];
};

const GroupField: FC<GroupFieldProps> = ({
    slots = [GroupFieldSlot.COLOR, GroupFieldSlot.LABEL],
}) => {
    const groupEntity = useRecordContext<EntityGroup>();

    if (!groupEntity) {
        return null;
    }

    const renderSlot = (slot: GroupFieldSlot): JSX.Element | null => {
        switch (slot) {
            case GroupFieldSlot.COLOR:
                return (
                    <Tooltip title={groupEntity.name}>
                        <StyledBox
                            ownerState={{ color: groupEntity.color }}
                        />
                    </Tooltip>
                );
            case GroupFieldSlot.LABEL:
                return (
                    <Typography>
                        {groupEntity.name}
                    </Typography>
                );
            default:
                return null;
        }
    };

    return (
        <Stack
            direction='row'
            spacing={1}
        >
            {
                slots.map((slot: GroupFieldSlot) => (
                    <Fragment key={slot}>
                        {renderSlot(slot)}
                    </Fragment>
                ))
            }
        </Stack>
    );
};

export default GroupField;
