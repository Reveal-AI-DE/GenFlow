// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Chip from '@mui/material/Chip';
import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import { useTranslate, Link } from 'react-admin';

import { WithTooltip } from '@/common';

type SignupButtonProps = object;

const SignupButton: FC<SignupButtonProps> = () => {
    const translate = useTranslate();

    return (
        <WithTooltip
            title={translate('action.sign_up')}
            trigger={(
                <span>
                    <Link
                        to='/signup'
                    >
                        <Chip
                            label={translate('action.sign_up')}
                            color='primary'
                            icon={<PersonAddAltIcon />}
                        />
                    </Link>
                </span>
            )}
            arrow
        />
    );
};

export default SignupButton;
