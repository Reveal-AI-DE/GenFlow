// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    FC, useCallback, useState, useEffect
} from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import { styled, useTheme } from '@mui/material/styles';
import {
    Datagrid, DateField, List, TextField, RecordContextProvider,
    FunctionField, Identifier, RowClickFunction, useDataProvider,
    useNotify,
} from 'react-admin';
import { matchPath, useLocation, useNavigate } from 'react-router';

import { Team, TeamRole } from '@/types';
import { UserField } from '@/user';
import { TeamCreateButton } from '@/team/form';
import TeamListAside from '@/team/list/TeamListAside';

const Root = styled(Box, {
    name: 'GFTeamListAside',
    slot: 'root',
})(({ theme }) => ({
    margin: theme.spacing(2),
    display: 'flex',
}));

const rowStyle = (selectedRow?: Identifier) => (record: Team) => {
    const theme = useTheme();
    let style = {};
    if (!record) {
        return style;
    }
    if (selectedRow && selectedRow === record.id.toString()) {
        style = {
            ...style,
            backgroundColor: theme.palette.action.selected,
        };
    }
    return style
};

type TeamListProps = object;

const TeamList: FC<TeamListProps> = () => {
    const dataProvider = useDataProvider();
    const location = useLocation();
    const navigate = useNavigate();
    const notify = useNotify();
    const match = matchPath('/teams/:id', location.pathname);
    const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);

    useEffect(() => {
        const fetchTeam = async (): Promise<void> => {
            dataProvider.getOne('teams', { id: match?.params.id })
                .then(({ data: team }) => setSelectedTeam(team))
                .catch(() => notify(
                    'ra.notification.http_error',
                    {
                        type: 'error',
                    }));
        }
        if (match && selectedTeam === null) {
            fetchTeam();
        }
    }, []);

    const rowClick: RowClickFunction = (_id, _resource, record) => {
        if (!record || record.is_personal) {
            return false;
        }
        if (!record || (record.user_role !== TeamRole.OWNER && record.user_role !== TeamRole.ADMIN)) {
            return false;
        }
        if (record.id === selectedTeam?.id) {
            setSelectedTeam(null);
            return 'list';
        }
        setSelectedTeam(record as unknown as Team);
        return 'edit';
    };

    const handleClose = useCallback(() => {
        navigate('/teams');
    }, [navigate]);

    return (
        <Root>
            <List
                exporter={false}
                actions={(
                    <TeamCreateButton />
                )}
                sx={{
                    flexGrow: 1,
                    transition: (theme: any) => theme.transitions.create(['all'], {
                        duration: theme.transitions.duration.enteringScreen,
                    }),
                }}
            >
                <Datagrid
                    rowClick={rowClick}
                    rowSx={rowStyle(
                        match ?
                            (match as any).params.id :
                            undefined,
                    )}
                    bulkActionButtons={false}
                >
                    <TextField source='name' />
                    <TextField source='description' sortable={false} />
                    <TextField source='user_role' />
                    <FunctionField
                        source='created_by'
                        render={(record) => (
                            <UserField user={record.owner} />
                        )}
                        sortable={false}
                    />
                    <DateField source='created_date' />
                </Datagrid>
            </List>
            <Drawer
                open={!!match}
                anchor='right'
                onClose={handleClose}
                sx={{ zIndex: 100 }}
            >
                {/* To avoid any errors if the route does not match,
                    we don't render at all the component in this case */}
                {!!match && selectedTeam && (
                    <RecordContextProvider value={selectedTeam}>
                        <TeamListAside />
                    </RecordContextProvider>
                )}
            </Drawer>
        </Root>
    );
};

export default TeamList;
