// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    Form, useTranslate,
    useGetResourceLabel,
    useResourceContext,
} from 'react-admin';

import { Dialog } from '@/common';
import GroupForm from '@/group/form/GroupForm';
import GroupFormActions from '@/group/form/GroupFormActions';

interface PromptGroupFormDialogProps {
    open: boolean;
    onClose: () => void;
};

const GroupFormDialog: FC<PromptGroupFormDialogProps> = ({
    open,
    onClose,
}) => {
    const translate = useTranslate();
    const getResourceLabel = useGetResourceLabel();
    const resource = useResourceContext();
    const title = resource ? (
        translate('action.add_new', {name: getResourceLabel(resource, 1)})
    ) : '';

    return (
        // TODO: <form> cannot appear as a descendant of <form>.
        <Form>
            <Dialog
                open={open}
                onClose={onClose}
                title={title}
                maxWidth='sm'
                dialogContent={(
                    <GroupForm />
                )}
                dialogAction={() => (
                    <GroupFormActions
                        onClose={onClose}
                    />
                )}
                fullWidth
            />
        </Form>
    );
};

export default GroupFormDialog;
