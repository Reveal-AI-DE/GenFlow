// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { RaRecord } from 'react-admin';

import { Identity } from '@/types/user';

export enum TeamRole {
    OWNER = 'owner',
    ADMIN = 'admin',
    ENGINEER = 'engineer',
    Member = 'member',
};

export interface Team extends RaRecord {
    name: string;
    description: string;
    status: string;
    user_role: TeamRole;
};

export interface Membership extends RaRecord {
    is_active: boolean;
    joined_date: number;
    role: string;
    user: Identity;
};
