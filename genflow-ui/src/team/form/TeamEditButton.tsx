// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import EditIcon from '@mui/icons-material/Edit';
import {
    useTranslate, EditBase, useRecordContext,
} from 'react-admin';

import { Team } from '@/types';
import { ButtonWithDialog } from '@/common';
import TeamForm from '@/team/form//TeamForm';
import TeamFormActions from '@/team/form/TeamFormActions';

type TeamEditButtonProps = object;

const TeamEditButton: FC<TeamEditButtonProps> = () => {
    const record = useRecordContext<Team>();

    if(!record) {
        return null;
    }

    const translate = useTranslate();

    return (
        <EditBase<Team>
            resource='teams'
            id={record.id}
            mutationMode='pessimistic'
            redirect={false}
        >
            <ButtonWithDialog
                label='ra.action.edit'
                startIcon={<EditIcon />}
                dialog={{
                    title: translate('label.edit_team', { name: record?.name }),
                    maxWidth: 'sm',
                    fullWidth: true,
                    disableBackdropClick: true,
                    ContentProps: {
                        dividers: true,
                    },
                    dialogContent: (
                        <TeamForm />
                    ),
                    dialogAction: (onClose) => (
                        <TeamFormActions
                            onClose={onClose}
                        />
                    ),
                }}
            />
        </EditBase>
    );
};

export default TeamEditButton;
