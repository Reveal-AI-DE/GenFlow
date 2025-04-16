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
    FilterButton, Button, FilterContextType,
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
    const { resource } = useListContext();
    const [isGrid, setIsGrid] = useState<boolean>(true);
    const getResourceLabel = useGetResourceLabel();
    const isSmall = useMediaQuery<Theme>((theme) => theme.breakpoints.down('md'));

    const onClick = (): void => {
        setIsGrid(!isGrid);
    };

    let width = '100%';
    if (isSmall) width = 'auto';
    if (aside) width = 'calc(100% - 16em)';

    return (
        <>
            <Title defaultTitle={getResourceLabel(resource, 2)} />
            {
                filters ? (
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
                ) : (
                    <TopToolbar>
                        {actions}
                        <Button onClick={onClick}>
                            {isGrid ? (<TableRowsIcon />) : (<GridViewIcon />)}
                        </Button>
                    </TopToolbar>
                )
            }
            <Box display='flex'>
                {aside}
                <Box width={width}>
                    {isGrid && <GridList {...rest} />}
                    {!isGrid && children}
                    <Pagination rowsPerPageOptions={[12, 24, 36, 60]} />
                </Box>
            </Box>
        </>
    );
};

export default ListGridSwitcher;
