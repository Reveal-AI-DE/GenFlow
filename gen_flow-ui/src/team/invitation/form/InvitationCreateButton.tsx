// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import RsvpIcon from '@mui/icons-material/Rsvp';
import {
    useTranslate, CreateBase, Form, useRecordContext,
} from 'react-admin';

import { ButtonWithDialog } from '@/common';
import { Team, MetaParams } from '@/types';
import InvitationForm from '@/team/invitation/form/InvitationForm';
import InvitationFormActions from '@/team/invitation/form/InvitationFormActions';

type InvitationCreateButtonProps = object;

const InvitationCreateButton: FC<InvitationCreateButtonProps> = () => {
    const team = useRecordContext<Team>();

    if (!team) {
        return null;
    }

    const meta: MetaParams = {
        queryParams: {
            team: team.id.toString(),
        },
    };

    const translate = useTranslate();

    return (
        <CreateBase
            resource='invitations'
            mutationOptions={{ meta: meta as any }}
        >
            <Form>
                <ButtonWithDialog
                    label='action.invite'
                    startIcon={<RsvpIcon />}
                    dialog={{
                        title: translate('label.invite'),
                        maxWidth: 'xs',
                        fullWidth: true,
                        disableBackdropClick: true,
                        ContentProps: {
                            dividers: true,
                        },
                        dialogContent: (
                            <InvitationForm />
                        ),
                        dialogAction: (onClose) => (
                            <InvitationFormActions
                                onClose={onClose}
                            />
                        ),
                    }}
                />
            </Form>
        </CreateBase>
    );
};

export default InvitationCreateButton;
