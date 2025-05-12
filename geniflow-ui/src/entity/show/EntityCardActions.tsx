// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useContext, ReactNode } from 'react';
import CardActions from '@mui/material/CardActions';
import EditIcon from '@mui/icons-material/Edit';
import {
    useRecordContext, useCreatePath, Link, useTranslate,
    DeleteWithConfirmButton, useResourceContext, RaRecord,
} from 'react-admin';

import { TeamRole } from '@/types';
import { GlobalContext, GlobalContextInterface } from '@/context';

export interface EntityInfoCardActionsProps {
    children?: ReactNode;
};

const EntityCardActions: FC<EntityInfoCardActionsProps> = ({
    children,
}) => {
    const entity = useRecordContext<RaRecord>();
    if (!entity) {
        return null;
    }

    const resource = useResourceContext();
    const translate = useTranslate();
    const createPath = useCreatePath();

    const { currentMembership } = useContext<GlobalContextInterface>(GlobalContext);
    const isOwnerOrAdmin = currentMembership?.role === TeamRole.OWNER || currentMembership?.role === TeamRole.ADMIN;

    if (!resource) {
        return null;
    }

    return (
        <CardActions disableSpacing>
            <Link
                to={
                    isOwnerOrAdmin ? (
                        createPath({
                            resource,
                            id: entity.id,
                            type: 'edit'
                        })) : ''
                }
                title={translate('ra.action.edit')}
            >
                <EditIcon
                    color={isOwnerOrAdmin ? 'primary' : 'disabled'}
                />
            </Link>
            {children}
            <DeleteWithConfirmButton
                label=''
                mutationMode='pessimistic'
                size='small'
                title={translate('ra.action.delete')}
                disabled={!isOwnerOrAdmin}
                sx={{
                    ml: 'auto',
                    minWidth: 'auto',
                }}
            />
        </CardActions>
    );
};

export default EntityCardActions;
