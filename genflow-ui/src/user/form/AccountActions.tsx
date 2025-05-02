// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Stack from '@mui/material/Stack';

import { ChangePasswordButton } from '@/user/form/button';

type AccountActionProps = object;

const AccountActions: FC<AccountActionProps> = () => (
    <Stack>
        <ChangePasswordButton />
    </Stack>
);

export default AccountActions;
