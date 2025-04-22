// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { TranslationMessages } from 'react-admin';
import englishMessages from 'ra-language-english';

const enUS: TranslationMessages = {
    ...englishMessages,
    resources: {
        users: {
            name: 'User |||| Users',
            fields: {
                username: 'Username',
                email: 'Email',
                password1: 'Password',
                password2: 'Confirm Password',
                first_name: 'First Name',
                last_name: 'Last Name',
                status: 'Status',
                created_date: 'Created At',
                updated_date: 'Updated At',
            },
        },
        sessions: {
            name: 'Session |||| Sessions',
            fields: {
                name: 'Name',
                session_type: 'Type',
                session_mode: 'Mode',
                related_model: {
                    label: 'Related Model',
                    provider_name: 'Provider',
                    model_name: 'Model',
                    config: {
                        parameters: 'Model Parameters',
                    }
                },
                related_prompt: 'Prompt',
                related_assistant: 'Assistant',
                owner: {
                    username: 'Created By',
                },
                created_date: 'Created At',
                updated_date: 'Updated At',
                usage: {
                    title: 'Usage',
                    total_messages: 'Total Messages',
                    total_tokens: 'Total Tokens',
                    total_price: 'Total Cost',
                    total_input_tokens: 'Input',
                    total_output_tokens: 'Output',
                    total_input_price: 'Input',
                    total_output_price: 'Output',
                    per_day: 'Daily Cost',
                }
            },
        },
        memberships: {
            name: 'Membership |||| Memberships',
            fields: {
                is_active: 'Active',
                joined_date: 'Joined Date',
                role: 'Role',
                status: {
                    label: 'Status',
                    invited: 'Invited on %{when} by %{by}',
                    joined: 'Joined on %{when}',
                    not_active: 'Not Active',
                }
            },
        },
        providers: {
            name: 'Provider |||| Providers',
            fields: {
            },
        },
        models: {
            name: 'Model |||| Models',
            fields: {
                type: 'Type',
            }
        },
        teams: {
            name: 'Team |||| Teams',
            fields: {
                name: 'Name',
                description: 'Description',
                user_role: 'Role',
                created_by: 'Created By',
                created_date: 'Created Date',
                updated_date: 'Updated Date',
            },
        },
        prompts: {
            name: 'Prompt |||| Prompts',
            fields: {
                name: 'Name',
                description: 'Description',
                type: 'Type',
                status: 'Status',
                pre_prompt: 'Prompt',
                q: 'Search name and description',
                group: {
                    id: 'Group',
                },
                related_model: {
                    label: 'Related Model',
                    provider_name: 'Provider',
                    model_name: 'Model',
                    config: {
                        parameters: 'Model Parameters',
                    }
                },
            },
        },
        'prompt-groups': {
            name: 'Prompt Group |||| Prompt Groups',
            fields: {}
        },
        assistants: {
            name: 'Assistant |||| Assistants',
            fields: {
                name: 'Name',
                description: 'Description',
                pre_prompt: 'Prompt',
                opening_statement: 'Starting Message',
                suggested_questions: 'Suggested Questions',
                status: 'Status',
                avatar: 'Avatar',
                q: 'Search name and description',
                related_model: {
                    label: 'Related Model',
                    provider_name: 'Provider',
                    model_name: 'Model',
                    config: {
                        parameters: 'Model Parameters',
                    }
                },
                collection_config: {
                    collection_id: 'Collection',
                },
                group: {
                    id: 'Group',
                },
            }
        },
        'assistant-groups': {
            name: 'Assistant Group |||| Assistant Groups',
            fields: {}
        },
    },
    label: {
        about: 'About',
        version: 'Version %{version}',
        settings: 'Settings',
        credentials: 'Credentials',
        enabled: 'Enabled',
        disabled: 'Disabled',
        advanced: 'Advanced',
        you: 'You',
        members: 'Members',
        view: 'View',
        total_resource: 'Total %{resource}',
        favorite_resources: 'Favorite Prompts and Assistants',
        files: 'Files',
        details: 'Details',
        session_info: 'Session Info',
        ask: 'Ask anything!',
        new: 'New Chat',
        chat: {
            title: 'Chat',
            actions: 'Chat Actions',
            info: 'Session Info',
            usage: 'Session Usage',
            input: {
                use_prompt: 'Use Prompt',
            },
            settings: {
                btn_label: 'Chat Settings',
                advanced: 'Advanced',
            },
        },
        collection: {
            interface: {
                step1: 'Collection Setup',
                step2: 'Vector Store Setup',
                step3: 'Files Upload'
            }
        },
        assistant: {
            interface: {
                step1: 'Assistant Setup',
                step2: 'Assistant Configuration',
                step3: 'Context Source',
                files: 'Uploaded Files',
                no_files: 'No files uploaded'
            },
        },
        invite: 'Invite Member',
        edit_member_dialog: 'Edit \'%{username}\' membership',
        edit_team: 'Edit \'%{name}\' Team',
    },
    message: {
        item_updated: '%{name} updated',
        delete_dialog: {
            disable_title: 'Disable %{resource}',
            disable_content: 'Are you sure you want to disable this %{resource}?',
            title: 'Delete \'%{name}\' %{resource}',
            content: 'Are you sure you want to delete this %{resource}?',
        },
        chat: {
            new: {
                title: 'Start new chat',
                description: 'by selecting LLM model, prompt or assistant ...',
            },
            bot: {
                title: 'Setup and send',
                description: 'a message to start chat ...',
            },
        },
        invited: 'Member invited',
        validate: {
            unique: '%{name} must be unique'
        },
        prompt: {
            start_test_title: 'Start Testing session',
            start_test_content: 'to verify the prompt ...',
        },
        related_deleted: 'Related %{resource} was deleted',
        register_success: 'User registered, please login to continue.',
        register_error: 'User registration failed, please try again.',
        no_teams: 'No teams available, please contact the administrator.',
        confirmed: 'Confirmed',
        email_confirmed: 'Your email has been confirmed. You can now log in.',
        not_confirmed: 'Incorrect Confirmation',
        email_not_confirmed: 'The confirmation link is incorrect or has expired. Please check your email for the correct link or request a new confirmation email.',
        verification_sent: 'Verification Email Sent',
        verification_email_sent: 'A verification email has been sent to your email address. Please check your inbox and follow the instructions to verify your account.',
    },
    action: {
        test: 'Test',
        setup: 'Setup',
        draft: 'Draft',
        back: 'Back',
        next: 'Next',
        upload: 'Upload',
        finish: 'Finish',
        publish: 'Publish',
        unpublish: 'Unpublish',
        invite: 'Invite',
        new_team: 'New Team',
        create: 'Create',
        add_new: 'Add New %{name}',
        setup_name: 'Setup %{name}',
        use: 'Use',
        pin: 'Mark as favorite',
        unpin: 'Unmark as favorite',
        copy: 'Copy',
        edit: 'Edit',
        regenerate: 'Regenerate',
        attach: 'Attach file',
        send: 'Send message',
        stop: 'Stop',
        scroll_top: 'Scroll to top',
        scroll_bottom: 'Scroll to bottom',
        sign_up: 'Sign Up',
        login_email: 'Use Email',
        login_username: 'Use Username',
        google_login: 'Login with Google',
    },
    validation: {
        not_available: 'Not available',
        password: {
            min: 'Password must contain at least %{number}% characters.',
            numeric: 'Password cannot be entirely numeric.',
            personal: 'Password cannot be too similar to your personal information.',
        }
    }
};

export default enUS;
