// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { DataProvider, UserIdentity } from 'react-admin';

export interface Identity extends UserIdentity {
    first_name: string;
    last_name: string;
};

export interface UserDataProvider extends DataProvider {
    check: () => Promise<boolean>;
};

export interface RegistrationFormData {
    username: string;
    email: string
    password1: string;
    password2: string;
};

export interface ChangePasswordFormData {
    old_password: string;
    new_password1: string
    new_password2: string;
};
