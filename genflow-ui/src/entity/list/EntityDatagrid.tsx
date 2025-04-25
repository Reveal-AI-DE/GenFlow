// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useContext } from 'react';
import {
    Datagrid, DatagridProps,
    BulkDeleteWithConfirmButton,
} from 'react-admin';
import { TeamRole } from '@/types';
import { GlobalContext, GlobalContextInterface } from '@/context';

const EntityBulkActionButtons: FC = () => (
    <BulkDeleteWithConfirmButton mutationMode='pessimistic' />
);

type EntityDatagridProps = Omit<DatagridProps, 'bulkActionButtons' | 'rowClick'>;

const EntityDatagrid: FC<EntityDatagridProps> = ({
    children,
    ...props
}: EntityDatagridProps) => {
    const { currentMembership } = useContext<GlobalContextInterface>(GlobalContext);
    const isOwnerOrAdmin = currentMembership?.role === TeamRole.OWNER || currentMembership?.role === TeamRole.ADMIN;

    return (
        <Datagrid
            {...props}
            bulkActionButtons={<EntityBulkActionButtons />}
            rowClick={isOwnerOrAdmin ? 'edit' : false}
        >
            {children}
        </Datagrid>
    );
};

export default EntityDatagrid;
