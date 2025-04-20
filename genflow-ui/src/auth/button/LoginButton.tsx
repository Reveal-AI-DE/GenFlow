// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Chip from '@mui/material/Chip';
import LoginIcon from '@mui/icons-material/Login';
import { useTranslate, Link } from 'react-admin';

import { WithTooltip } from '@/common';

type LoginButtonProps = object;

const LoginButton: FC<LoginButtonProps> = () => {
    const translate = useTranslate();

    return (
        <WithTooltip
            title={translate('ra.auth.sign_in')}
            trigger={(
                <span>
                    <Link
                        to='/login'
                    >
                        <Chip
                            label={translate('ra.auth.sign_in')}
                            color='primary'
                            icon={<LoginIcon />}
                        />
                    </Link>
                </span>
            )}
            arrow
        />
    );
};

export default LoginButton;
