// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { DataProvider, UserIdentity } from 'react-admin';

export interface Identity extends UserIdentity {
    first_name: string;
    last_name: string;
};

export interface UserDataProvider extends DataProvider {
    self: () => Promise<any>;
    check: () => Promise<boolean>;
};
