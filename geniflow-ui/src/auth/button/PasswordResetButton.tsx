// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { useTranslate, Link } from 'react-admin';

import { WithTooltip } from '@/common';

type PasswordResetButtonProps = object;

const PasswordResetButton: FC<PasswordResetButtonProps> = () => {
    const translate = useTranslate();

    return (
        <WithTooltip
            title={translate('action.forget_password')}
            trigger={(
                <span>
                    <Link
                        to='/auth/password-reset'
                    >
                        {translate('action.forget_password')}
                    </Link>
                </span>
            )}
            arrow
        />
    );
};

export default PasswordResetButton;
