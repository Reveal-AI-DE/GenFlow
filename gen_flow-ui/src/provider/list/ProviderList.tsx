// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import {
    ListBase, useListContext, Loading, RecordContextProvider
} from 'react-admin';

import { ProviderCard } from '@/provider/show';

const Root = styled(Box,{
    name: 'GFProviderList',
    slot: 'root',
})(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-start',
    margin: theme.spacing(1),
    gap: theme.spacing(1),
}));

const ProviderListView: FC = () => {
    const { data, isLoading } = useListContext();

    if (!data) return null;

    return (
        <Root>
            {isLoading ? (
                <Loading />
            ) : (
                data.map((record: any) => (
                    <RecordContextProvider value={record} key={record.id}>
                        <ProviderCard />
                    </RecordContextProvider>
                ))
            )}
        </Root>
    )
}

type ProviderListProps = object;

const ProviderList: FC<ProviderListProps> = () => (
    <ListBase resource='providers'>
        <ProviderListView />
    </ListBase>
);

export default ProviderList;
