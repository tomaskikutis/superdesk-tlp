/**
 * This is the default configuration file for the Superdesk application. By default,
 * the app will use the file with the name "superdesk.config.js" found in the current
 * working directory, but other files may also be specified using relative paths with
 * the SUPERDESK_CONFIG environment variable or the grunt --config flag.
 */
module.exports = function(grunt) {
    return {
        apps: [
            'anp',
            'superdesk-planning',
        ],
        importApps: [
            '../anp',
            'superdesk-planning',
        ],
        defaultRoute: '/workspace/monitoring',

        defaultTimezone: 'Europe/Amsterdam',
        shortTimeFormat: 'HH:mm, DD.MM.YYYY',
        shortDateFormat: 'HH:mm, DD.MM.YYYY',
        shortWeekFormat: 'HH:mm, DD.MM.YYYY',

        startingDay: '1',

        view: {
            timeformat: 'HH:mm',
            dateformat: 'DD.MM.YYYY',
        },
        
        list: {
            priority: [
                'priority'
            ],
            firstLine: [
                'wordcount',
                'slugline',
                'highlights',
                'markedDesks',
                'associations',
                'publish_queue_errors',
                'headline',
                'versioncreated'
            ],
            secondLine: [
                'profile',
                'state',
                'embargo',
                'update',
                'takekey',
                'signal',
                'flags',
                'updated',
                'desk',
                'fetchedDesk',
                'associatedItems',
                'nestedlink'
            ]
        },

        features: {
            preview: 1,
            swimlane: {defaultNumberOfColumns: 4},
            editor3: true,
            validatePointOfInterestForImages: false,
            editorHighlights: true,
            searchShortcut: true,
            editFeaturedImage: true,
            noMissingLink: true,
            nestedItemsInOutputStage: true,
            hideCreatePackage: true,
            planning: true,
        },
        workspace: {
            planning: true,
            assignments: true
        }
    };
};
