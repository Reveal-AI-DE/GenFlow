// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { subDays } from 'date-fns';

export const today = new Date();

export const lastMonthDays = Array.from({ length: 30 }, (_, i) => subDays(today, 29 - i));
