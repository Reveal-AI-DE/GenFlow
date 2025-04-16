// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useState, useContext } from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import SpeedDial from '@mui/material/SpeedDial';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import InfoIcon from '@mui/icons-material/Info';
import HardwareIcon from '@mui/icons-material/Hardware';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import AddCommentIcon from '@mui/icons-material/AddComment';
import ElectricMeterIcon from '@mui/icons-material/ElectricMeter';
import SettingsIcon from '@mui/icons-material/Settings';
import { useTranslate } from 'react-admin';

import { Popover } from '@/common';
import { SessionFloatActionKey } from '@/types';
import { SessionContext, SessionContextInterface } from '@/context';
import { SessionCard, SessionUsageCard } from '@/session';
import { ChatSettingForm } from '@/chat/form';

const StyledSpeedDial = styled(SpeedDial, {
    name: 'GFChatActions',
    slot: 'root',
})(({ theme }) => ({
    position: 'absolute',
    '&.MuiSpeedDial-directionDown, &.MuiSpeedDial-directionRight': {
        top: theme.spacing(2),
        right: theme.spacing(2),
    },
}));

const StyledBox = styled(Box, {
    name: 'GFChatActions',
    slot: 'popover-content',
})(({ theme }) => ({
    minWidth: '320px',
    maxWidth: '700px',
    maxHeight: '80vh',
    padding: theme.spacing(2),
}));

type ChatActionsProps = object;

const ChatActions: FC<ChatActionsProps> = () => {
    const [open, setOpen] = useState(false);
    const { floatActions } = useContext<SessionContextInterface>(SessionContext);

    const handleOpen = (): void => setOpen(true);

    const handleClose = (): void => setOpen(false);

    const translate = useTranslate();

    return (
        <StyledSpeedDial
            ariaLabel={translate('label.chat.actions')}
            icon={<SpeedDialIcon icon={<HardwareIcon />} />}
            direction='down'
            onClose={handleClose}
            onOpen={handleOpen}
            open={open}
        >
            {
                floatActions.includes(SessionFloatActionKey.SETTINGS) && (
                    <Popover
                        component='fab'
                        componentProps={{
                            icon: <SettingsIcon />,
                            tooltipTitle: translate('label.chat.settings.btn_label'),
                            open,
                        }}
                        anchorOrigin={{
                            vertical: 'top',
                            horizontal: 'left',
                        }}
                        transformOrigin={{
                            vertical: 'bottom',
                            horizontal: 'right',
                        }}
                    >
                        <StyledBox>
                            <ChatSettingForm />
                        </StyledBox>
                    </Popover>
                )
            }
            {
                floatActions.includes(SessionFloatActionKey.INFO) && (
                    <Popover
                        component='fab'
                        componentProps={{
                            icon: <InfoIcon />,
                            tooltipTitle: translate('label.chat.info'),
                            open,
                        }}
                        anchorOrigin={{
                            vertical: 'top',
                            horizontal: 'left',
                        }}
                        transformOrigin={{
                            vertical: 'bottom',
                            horizontal: 'right',
                        }}
                    >
                        <StyledBox>
                            <SessionCard />
                        </StyledBox>
                    </Popover>
                )
            }
            {
                floatActions.includes(SessionFloatActionKey.USAGE) && (
                    <Popover
                        component='fab'
                        componentProps={{
                            icon: <ElectricMeterIcon />,
                            tooltipTitle: translate('label.chat.usage'),
                            open,
                        }}
                        anchorOrigin={{
                            vertical: 'top',
                            horizontal: 'left',
                        }}
                        transformOrigin={{
                            vertical: 'bottom',
                            horizontal: 'right',
                        }}
                    >
                        <StyledBox>
                            <SessionUsageCard />
                        </StyledBox>
                    </Popover>
                )
            }
            {
                floatActions.includes(SessionFloatActionKey.NEW) && (
                    <SpeedDialAction
                        key={translate('label.new')}
                        icon={<AddCommentIcon sx={{transform: 'scaleX(-1)'}} />}
                        slotProps={{
                            tooltip: {
                                title: translate('label.new'),
                            },
                            fab: {
                                href: '/#/new',
                            }
                        }}
                    />
                )
            }
        </StyledSpeedDial>
    );
};

export default ChatActions;
