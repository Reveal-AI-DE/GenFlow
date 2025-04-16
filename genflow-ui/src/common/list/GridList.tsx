// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, ReactNode } from 'react';
import Skeleton from '@mui/material/Skeleton';
import Grid from '@mui/material/Grid2';
import Box from '@mui/material/Box';
import {
    useListContext, ListNoResults,
    RecordContextProvider,
} from 'react-admin';

import { useColsForWidth, times } from '@/utils';

type LoadingGridListProps = object;

const LoadingGridList: FC<LoadingGridListProps> = () => {
    const { perPage } = useListContext();
    const cols = useColsForWidth() * 8;

    return (
        <Grid container columns={cols} spacing={2}>
            {times(perPage, (key) => (
                <Grid key={key} size={8}>
                    <Skeleton
                        height='180px'
                        variant='rectangular'
                        animation='wave'
                    />
                </Grid>
            ))}
        </Grid>
    );
};

export interface GridListProps {
    ItemComponent: ReactNode;
};

const LoadedGridList: FC<GridListProps> = ({
    ItemComponent,
}) => {
    const { data, total } = useListContext();
    const cols = useColsForWidth() * 8;

    if (!data) return null;

    if (total === 0) return <ListNoResults />;

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Grid
                container
                columns={cols}
                spacing={2}
            >
                {data.map((record) => (
                    <Grid
                        key={record.id}
                        size={8}
                    >
                        <RecordContextProvider value={record}>
                            {ItemComponent}
                        </RecordContextProvider>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

const GridList: FC<GridListProps> = ({
    ItemComponent,
}) => {
    const { isPending } = useListContext();
    return isPending ? (
        <LoadingGridList />
    ) : (
        <LoadedGridList ItemComponent={ItemComponent} />
    );
};

export default GridList;
