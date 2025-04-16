// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import SaveIcon from '@mui/icons-material/Save';
import { DialogProps } from '@mui/material';
import {
    SaveButton, useNotify, useRefresh,
} from 'react-admin';
import { useFormContext } from 'react-hook-form';

import { CancelButton } from '@/common';

type MembershipFormActionsProps = {
    onClose: DialogProps['onClose'];
};

const MembershipFormActions: FC<MembershipFormActionsProps> = ({
    onClose,
}) => {
    const { reset } = useFormContext();
    const notify = useNotify();
    const refresh = useRefresh();

    return (
        <>
            <CancelButton
                onClick={() => {
                    reset();
                    if (onClose) {
                        onClose({}, 'escapeKeyDown');
                    }
                }}
            />
            <SaveButton
                label='ra.action.save'
                icon={<SaveIcon />}
                type='button'
                mutationOptions={{
                    onSuccess: () => {
                        notify('ra.notification.updated', { messageArgs: { smart_count: 1 } });
                        reset();
                        refresh();
                        if (onClose) {
                            onClose({}, 'escapeKeyDown');
                        }
                    }
                }}
            />
        </>
    );
};

export default MembershipFormActions;
