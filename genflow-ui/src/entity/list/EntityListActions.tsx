// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React from 'react';
import {
    ExportButton, CreateButton,
} from 'react-admin';

const EntityListActions = [
    <CreateButton key='create' />,
    <ExportButton key='export' />,
];

export default EntityListActions;
