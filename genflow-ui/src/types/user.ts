// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { DataProvider, UserIdentity } from 'react-admin';

export interface Identity extends UserIdentity {
    first_name: string;
    last_name: string;
};

export interface UserDataProvider extends DataProvider {
    self: () => Promise<any>;
    check: () => Promise<boolean>;
};
