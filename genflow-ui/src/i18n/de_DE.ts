// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { TranslationMessages } from 'react-admin';
import { formalGermanMessages } from '@haleos/ra-language-german';

const updatedFormalGermanMessages = {
    ...formalGermanMessages,
    ra: {
        ...formalGermanMessages.ra,
        page: {
            ...formalGermanMessages.ra.page,
            access_denied: 'Zugang verweigert',
            authentication_error: 'Authentication error',
        },
        message: {
            ...formalGermanMessages.ra.message,
            access_denied: 'Zugang verweigert',
            authentication_error: 'Authentication error',
            select_all_limit_reached:
                'Es gibt zu viele Elemente, um alle auszuwählen. Nur die ersten %{max} Elemente wurden ausgewählt.',
            placeholder_data_warning: 'Netzwerkproblem: Datenaktualisierung fehlgeschlagen.',
        },
        navigation: {
            ...formalGermanMessages.ra.navigation,
            clear_filters: 'Filter löschen',
            no_filtered_results: 'Mit den aktuellen Filtern wurde kein %{name} gefunden.',
        },
        action: {
            ...formalGermanMessages.ra.action,
            select_all_button: 'Alle auswählen',
        },
        auth: {
            ...formalGermanMessages.ra.auth,
            email: 'E-mail',
        }
    },
};

const deDE: TranslationMessages = {
    ...updatedFormalGermanMessages,
    resources: {
        users: {
            name: 'Benutzer |||| Benutzer',
            fields: {
                username: 'Benutzername',
                email: 'E-Mail',
                password1: 'Passwort',
                password2: 'Passwort bestätigen',
                first_name: 'Vorname',
                last_name: 'Nachname',
                status: 'Status',
                created_date: 'Erstellt am',
                updated_date: 'Aktualisiert am',
            },
        },
        sessions: {
            name: 'Session |||| Sessions',
            fields: {
                name: 'Name',
                session_type: 'Type',
                session_mode: 'Mode',
                related_model: {
                    label: 'Verwandtes Modell',
                    provider_name: 'Anbieter',
                    model_name: 'Modell',
                    config: {
                        parameters: 'Modell-Parameter',
                    }
                },
                related_prompt: 'Prompt',
                related_assistant: 'Assistent',
                owner: {
                    username: 'Erstellt von',
                },
                created_date: 'Erstellt am',
                updated_date: 'Updated At',
                usage: {
                    title: 'Nutzung',
                    total_messages: 'Gesamte Nachrichten',
                    total_tokens: 'Token insgesamt',
                    total_price: 'Gesamtkosten',
                    total_input_tokens: 'Input',
                    total_output_tokens: 'Output',
                    total_input_price: 'Input',
                    total_output_price: 'Output',
                    per_day: 'Tägliche Kosten',
                }
            },
        },
        memberships: {
            name: 'Mitgliedschaft |||| Mitgliedschaften',
            fields: {
                is_active: 'Aktive',
                joined_date: 'Beitrittsdatum',
                role: 'Rolle',
                status: {
                    label: 'Status',
                    invited: 'Eingeladen am %{when} durch %{by}',
                    joined: 'Beitritt am %{when}',
                    not_active: 'Nicht aktiv',
                }
            },
        },
        providers: {
            name: 'Anbieter |||| Anbieter',
            fields: {
            },
        },
        models: {
            name: 'Modell |||| Modelle',
            fields: {
                model_type: 'Typ',
            }
        },
        teams: {
            name: 'Team |||| Teams',
            fields: {
                name: 'Name',
                description: 'Beschreibung',
                user_role: 'Rolle',
                created_by: 'Erstellt von',
                created_date: 'Erstellt am',
                updated_date: 'Aktualisiertes am',
            },
        },
        prompts: {
            name: 'Prompt |||| Prompts',
            fields: {
                name: 'Name',
                description: 'Beschreibung',
                prompt_type: 'Type',
                prompt_status: 'Status',
                pre_prompt: 'Prompt',
                q: 'Suche nach Name und Beschreibung',
                group: {
                    id: 'Group',
                },
                related_model: {
                    label: 'Verwandtes Modell',
                    provider_name: 'Anbieter',
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
            name: 'Assistent |||| Assistenten',
            fields: {
                name: 'Name',
                description: 'Beschreibung',
                pre_prompt: 'Prompt',
                opening_statement: 'Start-Nachricht',
                suggested_questions: 'Vorgeschlagene Fragen',
                status: 'Status',
                avatar: 'Avatar',
                q: 'Suche nach Name und Beschreibung',
                related_model: {
                    label: 'Related Model',
                    provider_name: 'Anbieter',
                    model_name: 'Modell',
                    config: {
                        parameters: 'Modell-Parameters',
                    }
                },
                group: {
                    id: 'Group',
                },
            }
        },
        'assistant-groups': {
            name: 'Assistentengruppe |||| Assistentengruppen',
            fields: {}
        },
    },
    label: {
        about: 'Über',
        version: 'Version %{version}',
        settings: 'Einstellungen',
        credentials: 'Zugangsdaten',
        enabled: 'Aktiviert',
        disabled: 'Deaktiviert',
        advanced: 'Erweiterte',
        you: 'Du',
        members: 'Mitglieder',
        view: 'zeigen',
        total_resource: 'Anzahl der %{resource}',
        favorite_resources: 'Bevorzugte Prompts und Assistenten',
        files: 'Files',
        details: 'Details',
        session_info: 'Session Info',
        ask: 'Alles fragen!',
        new: 'Neuer Chat',
        chat: {
            title: 'Chat',
            actions: 'Chat-Aktionen',
            info: 'Session Info',
            usage: 'Sitzung Verwendung',
            input: {
                send: 'Nachricht senden',
                stop: 'stoppen',
                use_prompt: 'Prompt verwenden',
                placeholder: 'Alles fragen!'
            },
            settings: {
                btn_label: 'Chat-Einstellungen',
                advanced: 'Erweiterte',
            },
            scroll: {
                top: 'Nach oben scrollen',
                bottom: 'Nach unten scrollen',
            }
        },
        assistant: {
            step1: 'Assistent Einrichtung',
            step2: 'Assistent Konfiguration',
            step3: 'Dateien hochladen',
            files: 'Hochgeladene Dateien',
            no_files: 'Keine Dateien hochgeladen'
        },
        invite: 'Invite Member',
        edit_member_dialog: 'Edit \'%{username}\' membership',
        edit_team: 'Edit \'%{name}\' Team',
    },
    message: {
        item_updated: '%{name} aktualisiert',
        delete_dialog: {
            disable_title: ' %{resource} deaktivieren',
            disable_content: 'Sind Sie sicher, dass Sie diese %{resource} deaktivieren möchten? ?',
            title: 'Löschen \'%{name}\' %{resource}',
            content: 'Sind Sie sicher, dass Sie diese %{resource} löschen wollen??',
        },
        chat: {
            new: {
                title: 'Neuen Chat starten',
                description: 'durch Auswahl von LLM-Modell, Prompt oder Assistent ...',
            },
            bot: {
                title: 'Einrichten und Senden',
                description: 'eine Nachricht zum Starten des Chats ...',
            },
        },
        invited: 'Mitglied eingeladen',
        validate: {
            unique: '%{name} muss eindeutig sein'
        },
        team: {
            created: 'Team created',
            updated: 'Team aktualisiert',
        },
        prompt: {
            start_test_title: 'Start der Testsitzung',
            start_test_content: 'um die Prompt zu überprüfen ...',
        },
        related_deleted: 'Verwandte %{resource} wurde gelöscht.',
        register_success: 'Benutzer registriert, bitte melden Sie sich an, um fortzufahren.',
        register_error: 'Benutzerregistrierung fehlgeschlagen, bitte versuchen Sie es erneut.',
        no_teams: 'Keine Teams verfügbar, bitte wenden Sie sich an den Administrator.',
        confirmed: 'Bestätigt',
        email_confirmed: 'Ihre E-Mail wurde bestätigt. Sie können sich jetzt anmelden.',
        not_confirmed: 'Falsche Bestätigung',
        email_not_confirmed: 'Der Bestätigungslink ist falsch oder abgelaufen. Bitte überprüfen Sie Ihre E-Mails auf den richtigen Link oder fordern Sie eine neue Bestätigungs-E-Mail an.',
        verification_sent: 'Bestätigungs-E-Mail gesendet',
        verification_email_sent: 'Eine Bestätigungs-E-Mail wurde an Ihre E-Mail-Adresse gesendet. Bitte überprüfen Sie Ihren Posteingang und folgen Sie den Anweisungen, um Ihr Konto zu bestätigen.',
        image_not_supported: 'Nicht unterstütztes Bildformat oder Dateigröße überschreitet das Limit von 1 MB. Bitte laden Sie ein unterstütztes Bild mit weniger als 1 MB hoch.',
    },
    action: {
        test: 'Test',
        setup: 'einrichten',
        draft: 'entwurfen',
        back: 'Zurück',
        next: 'Nächste',
        upload: 'hochladen',
        finish: 'fertigstellen',
        publish: 'veröffentlichen.',
        invite: 'einladen',
        new_team: 'Neues Team',
        create: 'erstellen.',
        add_new: 'Neues hinzufügen %{name}',
        setup_name: 'einrichten %{name}',
        use: 'verwenden',
        copy: 'Kopie',
        edit: 'Bearbeiten',
        regenerate: 'Regenerieren',
        attach: 'Datei anhängen',
        send: 'Nachricht senden',
        stop: 'stoppen',
        sign_up: 'Registrieren',
        login_email: 'E-Mail verwenden',
        login_username: 'Benutzername verwenden',
        google_login: 'Mit Google anmelden',
    },
    validation: {
        not_available: 'Nicht verfügbar',
        password: {
            min: 'Das Passwort muss mindestens %{number} Zeichen enthalten.',
            numeric: 'Das Passwort darf nicht vollständig numerisch sein.',
            personal: 'Das Passwort darf nicht zu ähnlich zu Ihren persönlichen Informationen sein.',
        }
    }
};

export default deDE;
