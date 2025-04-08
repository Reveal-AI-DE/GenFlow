// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { RaRecord, DataProvider } from 'react-admin';

export interface Identity extends RaRecord {
    first_name: string;
};

export interface UserDataProvider extends DataProvider {
    self: () => Promise<any>;
};
