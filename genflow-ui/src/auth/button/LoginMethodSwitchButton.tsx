// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Chip from '@mui/material/Chip';
import EmailIcon from '@mui/icons-material/Email';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import Button, { ButtonProps} from '@mui/material/Button';
import { useTranslate } from 'react-admin';

import { WithTooltip } from '@/common';

interface LoginMethodSwitchButtonProps extends ButtonProps {
    loginMethod: 'email' | 'username';
};

const LoginMethodSwitchButton: FC<LoginMethodSwitchButtonProps> = ({
    loginMethod,
    onClick,
    ...rest
}) => {
    const translate = useTranslate();

    const title = loginMethod === 'username' ? translate('action.login_username') : translate('action.login_email');
    const label = loginMethod === 'username' ? translate('action.login_username') : translate('action.login_email');
    const icon = loginMethod === 'username' ? <AccountCircleIcon /> : <EmailIcon />;

    return (
        <WithTooltip
            title={title}
            trigger={(
                <span>
                    <Button
                        onClick={onClick}
                        {...rest}
                    >
                        <Chip
                            label={label}
                            color='primary'
                            icon={icon}
                        />
                    </Button>
                </span>
            )}
            arrow
        />
    );
};

export default LoginMethodSwitchButton;
