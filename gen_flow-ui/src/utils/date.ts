// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { subDays } from 'date-fns';

export const today = new Date();

export const lastMonthDays = Array.from({ length: 30 }, (_, i) => subDays(today, 29 - i));
