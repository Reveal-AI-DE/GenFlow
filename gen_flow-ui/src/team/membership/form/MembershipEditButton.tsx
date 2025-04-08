// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import EditIcon from '@mui/icons-material/Edit';
import {
    useTranslate, Form, EditBase, useRecordContext,
} from 'react-admin';

import { Membership } from '@/types';
import { ButtonWithDialog } from '@/common';
import MembershipForm from '@/team/membership/form/MembershipForm';
import MembershipFormActions from '@/team/membership/form/MembershipFormActions';

type MembershipEditButtonProps = object;

const MembershipEditButton: FC<MembershipEditButtonProps> = () => {
    const membership = useRecordContext<Membership>();
    if (!membership) {
        return null;
    }

    const translate = useTranslate();

    return (
        <EditBase
            resource='memberships'
            id={membership.id}
            mutationMode='pessimistic'
        >
            <Form>
                <ButtonWithDialog
                    label=''
                    startIcon={<EditIcon />}
                    size='small'
                    sx={{ minWidth: 'auto' }}
                    dialog={{
                        title: translate(
                            'label.edit_member_dialog',
                            {
                                username: membership.user.username
                            }),
                        maxWidth: 'xs',
                        fullWidth: true,
                        disableBackdropClick: true,
                        ContentProps: {
                            dividers: true,
                        },
                        dialogContent: (
                            <MembershipForm />
                        ),
                        dialogAction: (onClose) => (
                            <MembershipFormActions
                                onClose={onClose}
                            />
                        ),
                    }}
                />
            </Form>
        </EditBase>

    );
};

export default MembershipEditButton;
