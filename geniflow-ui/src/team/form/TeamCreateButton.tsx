// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import GroupAddIcon from '@mui/icons-material/GroupAdd';
import {
    useTranslate, CreateBase,
} from 'react-admin';

import { Team } from '@/types';
import { ButtonWithDialog } from '@/common';
import TeamForm from '@/team/form/TeamForm';
import TeamFormActions from '@/team/form/TeamFormActions';

type TeamCreateButtonProps = object;

const TeamCreateButton: FC<TeamCreateButtonProps> = () => {
    const translate = useTranslate();

    return (
        <CreateBase<Team>
            redirect={false}
        >
            <ButtonWithDialog
                label='action.new_team'
                startIcon={<GroupAddIcon />}
                dialog={{
                    title: translate('action.new_team'),
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
        </CreateBase>
    );
};

export default TeamCreateButton;
