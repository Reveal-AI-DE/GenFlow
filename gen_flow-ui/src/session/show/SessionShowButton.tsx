// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import RemoveRedEyeIcon from '@mui/icons-material/RemoveRedEye';
import {
    useTranslate, useCreatePath, Button,
    ButtonProps, useRedirect, useRecordContext,
} from 'react-admin';

import { Session } from '@/types';

const SessionShowButton: FC<ButtonProps> = ({
    label,
    ...rest
}) => {
    const record = useRecordContext<Session>();
    const redirect = useRedirect();
    const createPath = useCreatePath();
    const translate = useTranslate();

    if (!record) {
        return null;
    }

    return (
        <Button
            startIcon={<RemoveRedEyeIcon />}
            label={label ? translate(label) : ''}
            title={translate('label.view')}
            onClick={() => redirect(createPath({
                resource: 'sessions',
                id: record.id,
                type: 'show'
            }))}
            {...rest}
        />
    );
};

export default SessionShowButton;
