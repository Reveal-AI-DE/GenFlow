// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

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
