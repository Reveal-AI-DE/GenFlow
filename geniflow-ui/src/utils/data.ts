// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { DatasetType, DatasetElementType } from '@mui/x-charts/internals';
import { format } from 'date-fns';

import { SessionDailyUsage } from '@/types';
import { lastMonthDays } from '@/utils/date';

interface Option {
    id: string;
    name: string;
};

export const getChoicesFromEnum = (EnumType: any): Option[] => Object.keys(EnumType).map((key) => (
    { id: EnumType[key as keyof typeof EnumType], name: EnumType[key as keyof typeof EnumType] }
));

export const formatBytes = (bytes: number): string => {
    if (bytes < 1024) {
        return `${bytes} B`;
    } if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(0)}K`;
    } if (bytes < 1024 * 1024 * 1024) {
        return `${(bytes / (1024 * 1024)).toFixed(0)}M`;
    }
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(0)}G`;
};

export const truncateText = (
    text: string,
    limit: number,
    mode: 'words' | 'characters' = 'words'
): string => {
    if (mode === 'words') {
        const words = text.split(' ');
        if (words.length <= limit) {
            return text;
        }
        return `${words.slice(0, limit).join(' ')}...`;
    }
    if (text.length <= limit) {
        return text;
    }
    return `${text.slice(0, limit)}...`;
};

export const processDailyUsage = (usagePerDay: SessionDailyUsage[]): DatasetType => lastMonthDays.map((day) => {
    const key = format(new Date(day), 'yyyy-MM-dd');
    const usage: DatasetElementType<string | number | Date | null | undefined> = {
        day: key,
        total_messages: 0,
        total_price: 0,
    }
    const dayUsage = usagePerDay.find((u) => format(new Date(u.day), 'yyyy-MM-dd') === key);
    if (dayUsage) {
        usage.total_messages = dayUsage.total_messages;
        usage.total_price = dayUsage.total_price;
    }
    return usage;
});
