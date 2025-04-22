// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { useState, ReactElement } from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import useMediaQuery from '@mui/material/useMediaQuery';
import { Theme } from '@mui/material/styles';
import GridViewIcon from '@mui/icons-material/GridView';
import TableRowsIcon from '@mui/icons-material/TableRows';
import {
    Title,useListContext,
    Pagination, useGetResourceLabel, TopToolbar,
    Button, Empty, ListToolbar, FilterButton,
} from 'react-admin';

import GridList, { GridListProps } from './GridList';

interface ListGridSwitcherProps extends GridListProps {
    actions?: ReactElement[];
    filters?: ReactElement[];
    aside?: ReactElement;
    children?: ReactElement;
}

const ListGridSwitcher = ({
    actions, filters, aside, children, ...rest
}: ListGridSwitcherProps): JSX.Element => {
    const { resource, total, error } = useListContext();
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

        const updatedActions = (
            <TopToolbar>
                {filters && (
                    <FilterButton
                        filters={filters}
                        resource={resource}
                    />
                )}
                {actions}
                <Button onClick={onClick}>
                    {isGrid ? (<TableRowsIcon />) : (<GridViewIcon />)}
                </Button>
            </TopToolbar>
        );

        return (
            <ListToolbar
                filters={filters}
                actions={updatedActions}
            />

        );
    }

    const renderPagination = (): JSX.Element | null => (!error ? (
        <Pagination rowsPerPageOptions={[12, 24, 36, 60]} />
    ) : null);

    const renderNotEmpty = (): JSX.Element => (isGrid ? (
        <>
            <GridList {...rest} />
            {renderPagination()}
        </>
    ) : (
        <>
            <Card>
                {children}
            </Card>
            {renderPagination()}
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
