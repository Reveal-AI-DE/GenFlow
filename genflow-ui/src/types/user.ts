// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { FieldValues } from 'react-hook-form';
import { DataProvider, UserIdentity } from 'react-admin';

export interface Identity extends UserIdentity {
    first_name: string;
    last_name: string;
    last_login: string;
    date_joined: string;
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

interface BasePasswordFormData extends FieldValues {
    new_password1: string;
    new_password2: string;
};

export interface ChangePasswordFormData extends BasePasswordFormData {
    old_password: string;
};

export interface PasswordResetConfirmFormData extends BasePasswordFormData {
    uid: string
    token: string;
};

export interface PasswordResetFormData {
    email: string,
};
