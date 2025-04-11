// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import AddIcon from '@mui/icons-material/Add';
import SaveIcon from '@mui/icons-material/Save';
import { DialogProps } from '@mui/material';
import {
    useRecordContext, SaveButton, useNotify,
} from 'react-admin';
import { useFormContext } from 'react-hook-form';

import { Team } from '@/types';
import { CancelButton } from '@/common';

type TeamFormActionsProps = {
    onClose: DialogProps['onClose'];
};

const TeamFormActions: FC<TeamFormActionsProps> = ({
    onClose,
}) => {
    const record = useRecordContext<Team>();
    const { reset } = useFormContext();
    const notify = useNotify();

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
                label={record ? 'ra.action.save':'action.create'}
                type='button'
                mutationOptions={{
                    onSuccess: () => {
                        if (record) {
                            notify('ra.notification.updated', { messageArgs: { smart_count: 1 } });
                        } else {
                            notify('ra.notification.created');
                        }
                        reset();
                        if (onClose) {
                            onClose({}, 'escapeKeyDown');
                        }
                    }
                }}
                icon={record ? <SaveIcon />:<AddIcon />}
            />
        </>
    );
};

export default TeamFormActions;
