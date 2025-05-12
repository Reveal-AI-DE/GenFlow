// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React from 'react';
import { createRoot } from 'react-dom/client';

import './index.css';
import AppWrapper from './App';

const container = document.getElementById('root');
if (container) {
    const root = createRoot(container);
    root.render(<AppWrapper />);
}
