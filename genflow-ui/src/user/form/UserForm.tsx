// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { TextInput } from 'react-admin';

type UserFormProps = object;

const UserForm: FC<UserFormProps> = () => (
    <>
        <TextInput
            source='first_name'
        />
        <TextInput
            source='last_name'
        />
    </>
);

export default UserForm;
