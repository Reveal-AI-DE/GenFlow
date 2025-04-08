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
