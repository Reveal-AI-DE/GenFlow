// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React,
{
    FC,
    ReactNode
} from 'react';
import {
    styled
} from '@mui/material/styles';
import {
    Dialog as MuiDialog,
    DialogProps as MuiDialogProps
} from '@mui/material';
import DialogTitle from '@mui/material/DialogTitle';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import DialogContent,
{
    DialogContentProps as MuiDialogContentProps
} from '@mui/material/DialogContent';
import DialogActions,
{
    DialogActionsProps as MuiDialogActionsProps
} from '@mui/material/DialogActions';
import { Form } from 'react-admin';

const StyledDialogTitle = styled(DialogTitle, {
    name: 'GFDialog',
    slot: 'title',
})(({ theme }) => ({
    margin: 0,
    paddingRight: theme.spacing(2),
    paddingLeft: theme.spacing(2),
    paddingTop: theme.spacing(1),
    paddingBottom: theme.spacing(1),
}));

const StyledIconButton = styled(IconButton, {
    name: 'GFDialog',
    slot: 'close-icon',
})(({ theme }) => ({
    position: 'absolute',
    right: 8,
    top: 8,
    color: theme.palette.grey[500],
}));

interface DialogViewProps {
    title: string | ReactNode;
    dialogContent: ReactNode;
    dialogAction?: (onClose: MuiDialogProps['onClose']) => ReactNode;
    ContentProps?: MuiDialogContentProps;
    ActionsProps?: MuiDialogActionsProps;
    onClose: MuiDialogProps['onClose']
};

const DialogView: FC<DialogViewProps> = ({
    title,
    dialogContent,
    dialogAction,
    ContentProps,
    ActionsProps,
    onClose,
}) => (
    <>
        <StyledDialogTitle
            id='dialog-title'
        >
            {title}
        </StyledDialogTitle>
        <StyledIconButton
            aria-label='close'
            onClick={() => onClose && onClose({}, 'escapeKeyDown')}
        >
            <CloseIcon />
        </StyledIconButton>
        <DialogContent {...ContentProps}>
            {dialogContent}
        </DialogContent>
        {
            dialogAction && (
                <DialogActions {...ActionsProps}>
                    {dialogAction(onClose)}
                </DialogActions>
            )
        }
    </>
);

export interface DialogProps extends Omit<MuiDialogProps, 'title'> {
    title: string | ReactNode;
    dialogContent: ReactNode;
    dialogAction?: (onClose: MuiDialogProps['onClose']) => ReactNode;
    ContentProps?: MuiDialogContentProps;
    ActionsProps?: MuiDialogActionsProps;
}

const Dialog: FC<DialogProps> = ({
    onClose,
    open,
    title,
    dialogContent,
    dialogAction,
    ContentProps,
    ActionsProps,
    ...rest
}) => (
    <MuiDialog
        onClose={onClose}
        open={open}
        {...rest}
    >
        <DialogView
            title={title}
            dialogContent={dialogContent}
            dialogAction={dialogAction}
            ContentProps={ContentProps}
            ActionsProps={ActionsProps}
            onClose={onClose}
        />
    </MuiDialog>
);

export const FormDialog: FC<DialogProps> = ({
    onClose,
    open,
    title,
    dialogContent,
    dialogAction,
    ContentProps,
    ActionsProps,
    ...rest
}) => (
    <MuiDialog
        onClose={onClose}
        open={open}
        {...rest}
    >
        <Form>
            <DialogView
                title={title}
                dialogContent={dialogContent}
                dialogAction={dialogAction}
                ContentProps={ContentProps}
                ActionsProps={ActionsProps}
                onClose={onClose}
            />
        </Form>
    </MuiDialog>
);

export default Dialog;
