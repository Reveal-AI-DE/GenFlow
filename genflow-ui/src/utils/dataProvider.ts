// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

export const ResourceURL = (path: string | undefined, base = process.env.REACT_APP_BACKEND_API_BASE_URL): string => {
    if (path === undefined) return '';
    const parts = [base];
    parts.push(path.replace(/^\//, ''));
    return parts.join('/');
};

export const MediaURL = (path: string | undefined, base = process.env.REACT_APP_BACKEND_BASE_URL): string => (
    ResourceURL(path, base)
);
