// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React from 'react';
import { createRoot } from 'react-dom/client';

import './index.css';
import AppWrapper from './App';

const container = document.getElementById('root');
if (container) {
    const root = createRoot(container);
    root.render(<AppWrapper />);
}
