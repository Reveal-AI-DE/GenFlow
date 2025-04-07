// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { TranslationMessages } from 'react-admin';
import englishMessages from 'ra-language-english';

const enUS: TranslationMessages = {
    ...englishMessages,
    resources: {
        sessions: {
            name: 'Session |||| Sessions',
            fields: {
                name: 'Name',
                type: 'Type',
                mode: 'Mode',
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
                credentials: {
                    label: 'Credentials',
                    enabled: 'Enabled',
                    disabled: 'Disabled',
                }
            },
        },
        models: {
            name: 'Model |||| Models',
            fields: {
                model_type: 'Type',
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
        collections: {
            name: 'Collection |||| Collections',
            fields: {
                name: 'Name',
                description: 'Description',
                status: 'Status',
                embedding_model: {
                    label: 'Embedding Model',
                    provider_name: 'Provider',
                    model_name: 'Embedding Model',
                },
                chunk_config: 'Chunk Config',
                info: 'Vector Store Info',
            },
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
        providers: 'Providers',
        advanced: 'Advanced',
        members: 'Members',
        view: 'View',
        total_resource: 'Total %{resource}',
        favorite_resources: 'Favorite Prompts and Assistants',
        files: 'Files',
        collections: 'Collections',
        details: 'Details',
        samples: 'Samples',
        point: 'Point Id: %{id}',
        references: 'References',
        reference: 'Reference Id: %{id}',
        session: {
            new: 'New Chat',
        },
        chat: {
            title: 'Chat',
            actions: 'Chat Actions',
            info: 'Session Info',
            usage: 'Session Usage',
            input: {
                send: 'Send message',
                stop: 'Stop',
                attach: 'Attach file',
                use_prompt: 'Use Prompt',
                placeholder: 'Ask anything!'
            },
            settings: {
                btn_label: 'Chat Settings',
                advanced: 'Advanced',
            },
            scroll: {
                top: 'Scroll to top',
                bottom: 'Scroll to bottom',
            }
        },
        user_menu: {
            settings: {
                title: 'Settings',
            },
            about: {
                title: 'About',
            }
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
        membership: {
            invite: 'Invite Member',
            edit_dialog: 'Edit \'%{username}\' membership',
        },
        team: {
            edit_dialog: 'Edit \'%{name}\' Team',
        },
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
        team: {
            created: 'Team created',
            updated: 'Team updated',
        },
        prompt: {
            start_test_title: 'Start Testing session',
            start_test_content: 'to verify the prompt ...',
        }
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
    }
};

export default enUS;
