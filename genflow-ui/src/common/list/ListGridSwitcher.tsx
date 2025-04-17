// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { ReactNode, useState } from 'react';
import { Box, useMediaQuery, Theme } from '@mui/material';
import GridViewIcon from '@mui/icons-material/GridView';
import TableRowsIcon from '@mui/icons-material/TableRows';
import {
    Title, FilterContext, FilterForm, useListContext,
    Pagination, useGetResourceLabel, TopToolbar,
    FilterButton, Button, FilterContextType, Empty,
} from 'react-admin';

import GridList, { GridListProps } from './GridList';

interface ListGridSwitcherProps extends GridListProps {
    actions?: ReactNode[];
    filters?: FilterContextType;
    aside?: ReactNode;
    children?: ReactNode;
}

const ListGridSwitcher = ({
    actions, filters, aside, children, ...rest
}: ListGridSwitcherProps): JSX.Element => {
    const { resource, total } = useListContext();
    const [isGrid, setIsGrid] = useState<boolean>(true);
    const getResourceLabel = useGetResourceLabel();
    const isSmall = useMediaQuery<Theme>((theme) => theme.breakpoints.down('md'));

    const onClick = (): void => {
        setIsGrid(!isGrid);
    };

    let width = '100%';
    if (isSmall) width = 'auto';
    if (aside) width = 'calc(100% - 16em)';

    const renderTopBar = (): JSX.Element | null => {
        if (total === 0) return null;

        if (filters) {
            return (
                <FilterContext.Provider value={filters}>
                    <TopToolbar>
                        <FilterButton />
                        {actions}
                        <Button onClick={onClick}>
                            {isGrid ? (<TableRowsIcon />) : (<GridViewIcon />)}
                        </Button>
                    </TopToolbar>
                    <Box m={1} sx={{ '& form': { minHeight: 'auto' } }}>
                        <FilterForm />
                    </Box>
                </FilterContext.Provider>
            );
        }
        return (
            <TopToolbar>
                {actions}
                <Button onClick={onClick}>
                    {isGrid ? (<TableRowsIcon />) : (<GridViewIcon />)}
                </Button>
            </TopToolbar>
        );
    }

    const renderNotEmpty = (): JSX.Element => (isGrid ? (
        <>
            <GridList {...rest} />
            <Pagination rowsPerPageOptions={[12, 24, 36, 60]} />
        </>
    ) : (
        <>
            {children}
            <Pagination rowsPerPageOptions={[12, 24, 36, 60]} />
        </>
    ));

    const renderContent = (): JSX.Element => (total === 0 ? (
        <Empty />
    ) : (
        <Box display='flex'>
            {aside}
            <Box width={width}>
                {
                    renderNotEmpty()
                }
            </Box>
        </Box>
    ));

    return (
        <>
            <Title defaultTitle={getResourceLabel(resource, 2)} />
            {
                renderTopBar()
            }
            {
                renderContent()
            }

        </>
    );
};

export default ListGridSwitcher;
