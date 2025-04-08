// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import SendIcon from '@mui/icons-material/Send';
import { DialogProps } from '@mui/material';
import {
    SaveButton, useNotify, useRefresh,
} from 'react-admin';
import { useFormContext } from 'react-hook-form';

import { CancelButton } from '@/common';

type InvitationFormActionsProps = {
    onClose: DialogProps['onClose'];
};

const InvitationFormActions: FC<InvitationFormActionsProps> = ({
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
                label='action.invite'
                icon={<SendIcon />}
                type='button'
                mutationOptions={{
                    onSuccess: () => {
                        notify('message.invited');
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

export default InvitationFormActions;
