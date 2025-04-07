// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React from 'react';
import { Layout as RALayout, LayoutProps } from 'react-admin';

import AppBar from './AppBar';

const Layout = (props: LayoutProps): JSX.Element => (
    <RALayout {...props} appBar={AppBar} />
);

export default Layout;
